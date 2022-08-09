import json
from user_input_form import InputForm
from amino_acids import properties_hydropathy
from compute_blobs import (compute, clean_df)

from compute_snps import pathogenic_snps
import pandas as pd
import numpy as np
import time
import io
from matplotlib.backends.backend_svg import FigureCanvasSVG
import urllib.parse
import urllib.request

from flask import Flask, render_template, request, Response, session, jsonify, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_session import Session
import requests
from requests.adapters import HTTPAdapter, Retry
import re
import zlib
from xml.etree import ElementTree
from urllib.parse import urlparse, parse_qs, urlencode

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF




app = Flask(__name__)

CORS(app)  # To allow direct AJAX calls
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app) #This stores the user input for further calls

# URLs for API requests
REQUEST_URL_snp = "https://www.ebi.ac.uk/proteins/api/variation"
REQUEST_URL_features = "https://www.ebi.ac.uk/proteins/api/features"
REQUEST_UNIPROT_ID_FROM_ENSEMBL = "https://www.uniprot.org/uploadlists/"
   

@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm(request.form) #reads the user input

    if request.method == "POST":
        #checks if the user has provided uniprot id or residue sequence
        if "action_u" in request.form.to_dict(): #if uniprot id
            # get the disorder information for a given sequence
            uniprot_id = form.uniprot_id.data.splitlines()

            if len(uniprot_id) != 1 or len(uniprot_id[0].split()) != 1:
                return render_template("error.html",
                    title="More than one UniProt ID provided",
                    message="""It looks like you are querying about more than one protein.
                    We only support the blobulation of one protein at a time.""")

            user_uniprot_id = uniprot_id[0].strip()


            # Takes the input form, converts it to a dictionary, and requests the input type (from the dropdown menu selection) using the input_type key
            request_dict = request.form.to_dict()
            input_type = request_dict["input_type"]

            types = {"hgnc_id":"HGNC_ID", "ensembl_id":"Ensembl"}

            POLLING_INTERVAL = 3

            API_URL = "https://rest.uniprot.org"


            retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
            session = requests.Session()
            session.mount("https://", HTTPAdapter(max_retries=retries))


            def submit_id_mapping(from_db, to_db, ids):
                request = requests.post(
                    f"{API_URL}/idmapping/run",
                    data={"from": from_db, "to": to_db, "ids": ",".join(ids)},
                )
                request.raise_for_status()
                return request.json()["jobId"]


            def get_next_link(headers):
                re_next_link = re.compile(r'<(.+)>; rel="next"')
                if "Link" in headers:
                    match = re_next_link.match(headers["Link"])
                    if match:
                        return match.group(1)


            def check_id_mapping_results_ready(job_id):
                while True:
                    request = session.get(f"{API_URL}/idmapping/status/{job_id}")
                    request.raise_for_status()
                    j = request.json()
                    if "jobStatus" in j:
                        if j["jobStatus"] == "RUNNING":
                            print(f"Retrying in {POLLING_INTERVAL}s")
                            time.sleep(POLLING_INTERVAL)
                        else:
                            raise Exception(request["jobStatus"])
                    else:
                        return bool(j["results"] or j["failedIds"])


            def get_batch(batch_response, file_format, compressed):
                batch_url = get_next_link(batch_response.headers)
                while batch_url:
                    batch_response = session.get(batch_url)
                    batch_response.raise_for_status()
                    yield decode_results(batch_response, file_format, compressed)
                    batch_url = get_next_link(batch_response.headers)


            def combine_batches(all_results, batch_results, file_format):
                if file_format == "json":
                    for key in ("results", "failedIds"):
                        if key in batch_results and batch_results[key]:
                            all_results[key] += batch_results[key]
                elif file_format == "tsv":
                    return all_results + batch_results[1:]
                else:
                    return all_results + batch_results
                return all_results


            def get_id_mapping_results_link(job_id):
                url = f"{API_URL}/idmapping/details/{job_id}"
                request = session.get(url)
                request.raise_for_status()
                return request.json()["redirectURL"]


            def decode_results(response, file_format, compressed):
                if compressed:
                    decompressed = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
                    if file_format == "json":
                        j = json.loads(decompressed.decode("utf-8"))
                        return j
                    elif file_format == "tsv":
                        return [line for line in decompressed.decode("utf-8").split("\n") if line]
                    elif file_format == "xlsx":
                        return [decompressed]
                    elif file_format == "xml":
                        return [decompressed.decode("utf-8")]
                    else:
                        return decompressed.decode("utf-8")
                elif file_format == "json":
                    return response.json()
                elif file_format == "tsv":
                    return [line for line in response.text.split("\n") if line]
                elif file_format == "xlsx":
                    return [response.content]
                elif file_format == "xml":
                    return [response.text]
                return response.text


            def get_xml_namespace(element):
                m = re.match(r"\{(.*)\}", element.tag)
                return m.groups()[0] if m else ""


            def merge_xml_results(xml_results):
                merged_root = ElementTree.fromstring(xml_results[0])
                for result in xml_results[1:]:
                    root = ElementTree.fromstring(result)
                    for child in root.findall("{http://uniprot.org/uniprot}entry"):
                        merged_root.insert(-1, child)
                ElementTree.register_namespace("", get_xml_namespace(merged_root[0]))
                return ElementTree.tostring(merged_root, encoding="utf-8", xml_declaration=True)


            def print_progress_batches(batch_index, size, total):
                n_fetched = min((batch_index + 1) * size, total)
                print(f"Fetched: {n_fetched} / {total}")


            def get_id_mapping_results_search(url):
                parsed = urlparse(url)
                query = parse_qs(parsed.query)
                file_format = query["format"][0] if "format" in query else "json"
                if "size" in query:
                    size = int(query["size"][0])
                else:
                    size = 500
                    query["size"] = size
                compressed = (
                    query["compressed"][0].lower() == "true" if "compressed" in query else False
                )
                parsed = parsed._replace(query=urlencode(query, doseq=True))
                url = parsed.geturl()
                request = session.get(url)
                request.raise_for_status()
                results = decode_results(request, file_format, compressed)
                total = int(request.headers["x-total-results"])
                print_progress_batches(0, size, total)
                for i, batch in enumerate(get_batch(request, file_format, compressed), 1):
                    results = combine_batches(results, batch, file_format)
                    print_progress_batches(i, size, total)
                if file_format == "xml":
                    return merge_xml_results(results)
                return results


            def get_id_mapping_results_stream(url):
                if "/stream/" not in url:
                    url = url.replace("/results/", "/results/stream/")
                request = session.get(url)
                request.raise_for_status()
                parsed = urlparse(url)
                query = parse_qs(parsed.query)
                file_format = query["format"][0] if "format" in query else "json"
                compressed = (
                    query["compressed"][0].lower() == "true" if "compressed" in query else False
                )
                return decode_results(request, file_format, compressed)

            for input_key in types:
                if input_type == input_key:
                    print(input_key)
                    job_id = submit_id_mapping(
                        from_db=input_key, to_db="UniProtKB", ids=[user_uniprot_id]
                    )
                    if check_id_mapping_results_ready(job_id):
                        link = get_id_mapping_results_link(job_id)
                        results = get_id_mapping_results_search(link)
                        # Equivalently using the stream endpoint which is more demanding
                        # on the API and so is less stable:
                        # results = get_id_mapping_results_stream(link)
                        user_uniprot_id = results['results'][0]['to']['primaryAccession']

            try:
                response_d2p2 = requests.get(
                    f'http://d2p2.pro/api/seqid/["{user_uniprot_id}"]'
                )
                data_d2p2 = response_d2p2.json()
            except:
                data_d2p2 = {user_uniprot_id: []}

            # get the sequence and its name from uniprot database, perform error checks
            uniprot_params = {
                "offset": 0,
                "size": -1,
                "consequencetype": "missense",
                "accession": user_uniprot_id,
            }
            try:
                get_sequence = requests.get(
                    REQUEST_URL_features,
                    params=uniprot_params,
                    headers={"Accept": "application/json"},
                )
            except ConnectionError:
                return render_template("error.html",
                    title="Unable to connect to UniProt server",
                    message="""There is probably an intermittent network error from our server to theirs.
                    If the UniProt server is down then this service won't work either.
                    Please try again later.""")
            seq_file = get_sequence.json()

            if 'errorMessage' in seq_file:
                return render_template("error.html",
                    title="UniProt server returned an error",
                    message=f"""The UniProt server said: {', '.join(seq_file['errorMessage'])}""")

            get_snp = requests.get(
                REQUEST_URL_snp,
                params=uniprot_params,
                headers={"Accept": "application/json"},
            )
            # HTTP status code 200 means the request was successful
            if get_snp.status_code != 200:
                return render_template("error.html",
                    title="Error getting SNP from UniProt",
                    message="""There was an error retrieving SNP data from UniProt""")

            seq_file_snp = get_snp.json()

            if seq_file_snp:
                snps_json = pathogenic_snps (seq_file_snp[0]["features"]) #filters the disease causing SNPs
            else:
                snps_json = "[]"
            my_seq = seq_file[0]["sequence"]

            if (
                user_uniprot_id not in data_d2p2
                or len(data_d2p2[user_uniprot_id]) == 0
            ):
                disorder_residues = [0]

            else:
                try:
                    disorder_file = data_d2p2[user_uniprot_id][0][2]["disorder"]["disranges"] #filters the disorder residues from d2p2, PV2 predictor
                    df2 = pd.DataFrame(disorder_file, columns=['predictor', 'beg', 'end'])
                    df3 = df2.loc[df2['predictor'] == 'PV2'] #uses only PV2 predictor from d2p2
                    df3 = df3.astype({'beg': int, 'end': int})
                    df3['disorder_residues'] = list(zip(df3['beg'], df3['end']))
                    df3['disorder_residues'] = df3['disorder_residues'].apply(lambda x: list(range(x[0],x[-1]+1)))
                    df4 = df3.sum(axis=0)
                    disorder_residues = df4['disorder_residues']
                except IndexError:
                    disorder_residues = [0]

            # Blobulation
            window = 3 
            session['sequence'] = str(my_seq) #set the current sequence variable
            my_initial_df = compute(
                str(my_seq), float(0.4), 4, window=window, disorder_residues=disorder_residues
            )
            #define the data frame (df)
            df = my_initial_df
            chart_data = df.round(3).to_dict(orient="records")
            chart_data = json.dumps(chart_data, indent=2)
            data = {"chart_data": chart_data}
            return render_template(
                    "result.html",
                    data=data,
                    form=form,
                    my_cut=0.4,
                    my_snp=snps_json,
                    my_uni_id="'%s'" % user_uniprot_id,
                    my_seq="'%s'" % my_seq,
                    my_seq_download="%s" % my_seq,
                    domain_threshold=4,
                    domain_threshold_max=len(str(my_seq)),
                    my_disorder = str(disorder_residues).strip('[]'),
                    activetab = '#result-tab'
                )

        else: # if the user inputs amino acid sequence
            aa_sequence = form.aa_sequence.data.splitlines()
            if len(aa_sequence) > 1:
                return render_template("error.html",
                    title="More than one sequence provided",
                    message="""It looks like you are querying about more than one sequence.
                    We only support one sequence at a time.""")

            # Make everything upper case 
            my_seq = aa_sequence[0].strip().upper()
            session['sequence'] = str(my_seq)


            # Ensure that all characters in sequence actually represent amino acids
            if any(x not in properties_hydropathy for x in my_seq):
                return render_template("error.html",
                    title='Invalid characters in sequence',
                    message="""The protein sequence you supplied contains non-amino-acid characters.
                    It should consist only of single-letter amino acid sequence codes.""")
            # do the blobulation
            window = 3
            my_initial_df = compute(
                str(my_seq), float(0.4), 4, window=window
            )  # blobulation
            df = my_initial_df
            chart_data = df.round(3).to_dict(orient="records")
            chart_data = json.dumps(chart_data, indent=2)
            data = {"chart_data": chart_data}
            return render_template(
                "result.html",
                data=data,
                form=form,
                my_cut=0.4,
                my_snp="[]",
                my_uni_id="'%s'" % form.seq_name.data,
                my_seq="'%s'" % my_seq,
                my_seq_download="%s" % my_seq,
                domain_threshold=4,
                domain_threshold_max=len(str(my_seq)),
                my_disorder = '0',
                activetab = '#result-tab'
            )
    else:
         #creates the HTML layout of the home page along with user input fields
        return render_template("index.html", form=form, activetab='#home-tab')



@app.route('/api/query', methods=['GET'])
def api_id():
    """This can be used for api calling {blobulator_link}/api/query?my_seq=AAAA&domain_threshold=24&cutoff=0.5&my_disorder=2,3"""
    my_seq  = str(request.args['my_seq'])
    domain_threshold  = request.args['domain_threshold']
    cutoff  = request.args['cutoff']
    my_disorder  = request.args['my_disorder']
    #print (my_disorder.split(","))
    my_disorder = list(map(int, my_disorder.split(",")))

    window = 3
    my_initial_df = compute(
        str(my_seq),
        float(cutoff),
        float(domain_threshold),
        window=window,
        disorder_residues = list(my_disorder),
    )  # blobulation
    df = my_initial_df
    #df = df.drop(range(0, 1))
    chart_data = df.round(3).to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)
    data = {"chart_data": chart_data}
    return data

@app.route('/postmethod', methods=['POST'])
def get_post():
    """This method is used to update the data when the slider is moved in index.html"""
    my_seq  = request.form['my_seq']
    domain_threshold  = request.form['domain_threshold']
    cutoff  = request.form['cutoff']
    my_disorder  = request.form['my_disorder']
    my_disorder  = list(map(int, my_disorder.split(",")))
    window = 3
    my_initial_df = compute(
        str(my_seq),
        float(cutoff),
        float(domain_threshold),
        window=window,
        disorder_residues = list(my_disorder),
    )  # blobulation
    df = my_initial_df
    #df = df.drop(range(0, 1))
    chart_data = df.round(3).to_dict(orient="records")
    chart_data = json.dumps(chart_data, indent=2)
    #print (jsonify(chart_data))
    data = {"chart_data": chart_data}
    return (data)


@app.route("/json", methods=["GET", "POST"]
)
def calc_json():
    """This method is used to blobulate and adds the data to data download option"""
    form = InputForm(request.form) #reads the user input
    #print(request.form)
    user_input = form.uniprot_id.data.splitlines()
    my_seq  = request.form['my_seq']
    domain_threshold  = request.form['domain_threshold']
    cutoff  = request.form['cutoff']
    my_disorder  = request.form['my_disorder']
    my_disorder  = list(map(int, my_disorder.split(",")))
    window = 3
    my_initial_df = compute(
        str(my_seq),
        float(cutoff),
        float(domain_threshold),
        window=window,
        disorder_residues = list(my_disorder),
    )  # blobulation
    df = my_initial_df
    df = clean_df(df)
    
    #f = "##" + str(user_input) + "\n" + str(df.round(1).to_csv(index=False))
    f = str(df.round(1).to_csv(index=False))
    
    return Response(f,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=data.csv"})


@app.route("/plot", methods=["GET", "POST"])
def calc_plot():
    """This method is used to add the blobulation plot to figure download option"""
    if request.method == "POST":
        #my_seq  = request.form['my_seq']
        my_seq = request.args['my_seq']
        domain_threshold  = request.form['domain_threshold']
        cutoff  = request.form['cutoff']
        my_disorder  = request.form['my_disorder']
        my_disorder  = list(map(int, my_disorder.split(",")))
        window = 3
        fig = compute(
            str(my_seq),
            float(cutoff),
            float(domain_threshold),
            window=window, my_plot =True,disorder_residues = list(my_disorder)
        )  # blobulation
        output = io.BytesIO()
        FigureCanvasSVG(fig).print_svg(output)
        return Response(output, mimetype="image/svg+xml", headers={"Content-disposition":
                   "attachment; filename=plot.svg", "Cache-Control": "no-store"})
    else:
        #my_seq  = request.form['my_seq']
        my_seq = session.get('sequence')
        domain_threshold  = request.args['domain_threshold']
        cutoff  = request.args['cutoff']
        my_disorder  = [0]
        window = 3
        fig = compute(
            str(my_seq),
            float(cutoff),
            float(domain_threshold),
            window=window, my_plot =True,disorder_residues = list(my_disorder)
        )  # blobulation
        output_svg = io.BytesIO()
        FigureCanvasSVG(fig).print_svg(output_svg)
        # Must seek to beginning of file or svg2rlg will try to read past end of file and produce null output
        output_svg.seek(0)
        drawing = svg2rlg(output_svg)
        output_pdf = io.BytesIO()
        renderPDF.drawToFile(drawing, output_pdf)

        return Response(output_pdf.getvalue(), mimetype="image/pdf", headers={"Content-disposition":
                   "attachment; filename=plot.pdf", "Cache-Control": "no-store"})

if __name__ == "__main__":
    app.run(debug=True)