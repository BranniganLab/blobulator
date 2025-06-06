import json

import os
import datetime
from user_input_form import InputForm
from blobulator.amino_acids import properties_hydropathy
from blobulator.compute_blobs import (compute, clean_df)
from blobulator.compute_snps import pathogenic_snps

from Bio.PDB import PDBParser
from Bio.PDB import PPBuilder
from Bio.PDB.PDBIO import PDBIO
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import pandas as pd
import numpy as np
import time
import io
from io import StringIO
from matplotlib.backends.backend_svg import FigureCanvasSVG
import urllib.parse
import urllib.request
import tempfile
import pathlib

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

from importlib import reload

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

template_dir = os.path.abspath('../website/templates')
app = Flask(__name__, template_folder=template_dir)

CORS(app)  # To allow direct AJAX calls
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app) #This stores the user input for further calls

# URLs for API requests
REQUEST_URL_snp = "https://www.ebi.ac.uk/proteins/api/variation"
REQUEST_URL_features = "https://www.ebi.ac.uk/proteins/api/features"
REQUEST_UNIPROT_ID_FROM_ENSEMBL = "https://www.uniprot.org/uploadlists/"
REQUEST_URL_coordinates = "https://www.ebi.ac.uk/proteins/api/coordinates"

# Wait this many seconds, max
REQUEST_TIMEOUT = 10

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
            user_uniprot_id_original = uniprot_id[0].strip()

            # Takes the input form, converts it to a dictionary, and requests the input type (from the dropdown menu selection) using the input_type key
            request_dict = request.form.to_dict()
            input_type = request_dict["input_type"]

            types = {"ensembl_id":"Ensembl"}

            for input_key in types:
                ## If we've got a non-uniprot ID,
                if input_type == input_key: 
                    ## Convert to uniprot
                    import uniprot_id_lookup
                    reload(uniprot_id_lookup)
                    try:
                        converted_id = uniprot_id_lookup.results['results'][0]['to']['primaryAccession']
                        user_uniprot_id = converted_id
                        original_accession = str(types[input_key]) + " ID: " + user_uniprot_id_original
                    except:
                        return render_template("error.html",
                        title="ID Error",
                        message="""There seems to be an error with the ID you've entered. Check your ID and try again.""")
                else:
                    original_accession = ""

            # get the sequence and its name from uniprot database, perform error checks
            uniprot_params = {
                "offset": 0,
                "size": -1,
                "consequencetype": "missense",
                "accession": user_uniprot_id,
            }

            # We define a nested function that we'll call below using a thread pool
            def fetch_json(args):
                tag, url, params = args
                try:
                    data = requests.get(
                        url,
                        params=params,
                        headers={"Accept": "application/json"},
                        timeout=REQUEST_TIMEOUT # NB: This is where we tweak the timeout. 
                    )
                except:
                    return tag, None
                
                return tag, data.json()

            # We have a list of request URLs and parameters. Each one is annotated by a "tag" which is just the first
            # string in each tuple. We'll use this tag to identify which result data goes with what request
            fetch_args = [
                ('D2P2', f'http://d2p2.pro/api/seqid/["{user_uniprot_id}"]', []),
                ('Feature', REQUEST_URL_features, uniprot_params),
                ('SNP', REQUEST_URL_snp, uniprot_params),
                ('Coordinates', REQUEST_URL_coordinates, uniprot_params),
            ]

            # The ThreadPoolExecutor has a submit method that dispatches the function we specified (fetch_json)
            # multiple times concurrently. It immediately returns a "future" which gets resolved by the as_completed
            # method, which I guess returns the next available result when it is called, or blocks waiting for one
            fetched_data = {}
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(fetch_json, args) for args in fetch_args]
                for future in as_completed(futures):
                    try:
                        tag, data = future.result()
                        fetched_data[tag] = data
                    except ValueError as e:
                        # print(f"Task generated exception: {e}")
                        fetched_data[tag] = None
                
            # At this point fetched data is full of either our data, or Nones for each thing we called
            data_d2p2 = fetched_data['D2P2']
            seq_file = fetched_data['Feature']
            seq_file_snp = fetched_data['SNP']
            seq_file_coords = fetched_data['Coordinates']

            if 'errorMessage' in seq_file:
                return render_template("error.html",
                    title="UniProt server returned an error",
                    message=f"""The UniProt server said: {', '.join(seq_file['errorMessage'])}""")
            
            if 'errorMessage' in seq_file_snp:
                return render_template("error.html",
                    title="UniProt server returned an error",
                    message=f"""The UniProt server said: {', '.join(seq_file_snp['errorMessage'])}""")

            # Now we can process the fetched data
            if seq_file_snp:
                snps_json = pathogenic_snps(seq_file_snp[0]["features"]) #filters the disease causing SNPs
            else:
                snps_json = "[]"

            my_seq = seq_file[0]["sequence"]

            if (data_d2p2 is None) or (user_uniprot_id not in data_d2p2 or len(data_d2p2[user_uniprot_id]) == 0):
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

            try:
                protein_name = seq_file[0]['features'][0]['description']
                if len(protein_name) == 0:
                    user_uniprot_name = ""
                    user_uniprot_entry = ""
                else:
                    user_uniprot_name = "Protein Details: " + str(protein_name)
                    user_uniprot_entry = "Uniprot Entry: " + str(seq_file[0]['entryName'])
            except IndexError:
                user_uniprot_name = ''
                user_uniprot_entry = ''

            try:
                gn_chrom = seq_file_coords[0]['gnCoordinate'][0]['genomicLocation']['chromosome']
                gn_start = seq_file_coords[0]['gnCoordinate'][0]['genomicLocation']['exon'][0]['genomeLocation']['begin']['position']
                gn_end = seq_file_coords[0]['gnCoordinate'][0]['genomicLocation']['exon'][0]['genomeLocation']['end']['position']
                strand_sign = '+' if np.sign(gn_start - gn_end) == 1 else '-'
                hg_identifier = 'Genomic Location (GRCh Build 38, longest transcript): ' + str(gn_chrom) + ': ' + str(gn_start) + '-'+ str(gn_end) + " (" + strand_sign + ")"
            except:
                hg_identifier = ""

            # if seq_file_snp:
            #     snps_json = pathogenic_snps (seq_file_snp[0]["features"]) #filters the disease causing SNPs
            # else:
            #     snps_json = "[]"

            #Blobulation
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
            shift = 0
            return render_template(
                    "result.html",
                    data=data,
                    form=form,
                    my_cut=0.4,
                    my_snp=snps_json,
                    my_uni_id="'%s'" % user_uniprot_id,
                    my_uni_id_linked= "ID: <a href=https://www.uniprot.org/uniprotkb/" + user_uniprot_id + ' target="_blank">' + user_uniprot_id + '</a>',
                    my_seq="'%s'" % my_seq,
                    my_seq_download="%s" % my_seq,
                    domain_threshold=4,
                    domain_threshold_max=len(str(my_seq)),
                    my_disorder = str(disorder_residues).strip('[]'),
                    activetab = '#result-tab',
                    my_name = user_uniprot_name,
                    my_entry_name = user_uniprot_entry,
                    my_original_id = original_accession,
                    my_hg_value = hg_identifier,
                    chain = '',
                    pdb_string = '',
                    shift=shift
                )

        ## If we have a pdb upload
        elif "action_p" in request.form.to_dict():
            print(request.form.to_dict)
            pdb_file = request.files["pdb_file"].read()
            chain = request.form['chain_select']

            my_seq, shift, saved_chain, pdb_string = read_pdb_file(pdb_file, chain)
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
                my_uni_id_stripped="ID: " + form.seq_name.data,
                my_seq="'%s'" % my_seq,
                my_seq_download="%s" % my_seq,
                domain_threshold=4,
                domain_threshold_max=len(str(my_seq)),
                my_disorder = '0',
                activetab = '#result-tab',
                chain = saved_chain,
                pdb_string = pdb_string,
                shift=shift
            )

            

        else: # if the user inputs amino acid sequence
            aa_sequence_list = form.aa_sequence.data.splitlines()
            aa_sequence = "".join([str(item) for item in aa_sequence_list])
            # if len(aa_sequence) > 1:
            #     return render_template("error.html",
            #         title="More than one sequence provided",
            #         message="""It looks like you are querying about more than one sequence.
            #         We only support one sequence at a time.""")

            # Make everything upper case 
            my_seq = aa_sequence.strip().upper()
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
            shift = 0
            return render_template(
                "result.html",
                data=data,
                form=form,
                my_cut=0.4,
                my_snp="[]",
                my_uni_id="'%s'" % form.seq_name.data,
                my_uni_id_stripped="ID: " + form.seq_name.data,
                my_seq="'%s'" % my_seq,
                my_seq_download="%s" % my_seq,
                domain_threshold=4,
                domain_threshold_max=len(str(my_seq)),
                my_disorder = '0',
                activetab = '#result-tab',
                chain = '',
                pdb_string = '',
                shift=shift
            )
    else:
         #creates the HTML layout of the home page along with user input fields
        return render_template("index.html", form=form, activetab='#home-tab')


def extract_chain(chain, temporary_pdb_file, io, structure):
    """
    Extract a single chain from a PDB file and save it as a temporary PDB file

    Parameters
    ----------
    chain : str
        The name of the chain to extract
    temporary_pdb_file : str
        The temporary PDB file to save the chain to
    io : PDBIO
        The PDBIO object to use for saving the temporary PDB file
    structure : PDBStructure
        The PDBStructure object containing the chains

    Returns
    -------
    my_seq : str
        The sequence of the extracted chain
    shift : int
        The shift in residue numbering required to match the PDB file
    saved_chain : str
        The chain id of the saved chain
    pdb_string : str
        The contents of the temporary PDB file as a string
    """
    chain_count = 0
            ## Use biopython's pdb get chains function to iterate through their structures, and pdb I/O to load only the structure of one into molstar
    for current_chain in structure.get_chains():
                ## Save the first chain
        if chain_count == 0:
            io.set_structure(current_chain)
            saved_chain = current_chain.id
            
                ## If the user selected chain matches the current chain, save it instead
                ## Save the temporary pdb file because biopython requires a file to exist
        elif current_chain.id == chain:
            io.set_structure(current_chain)
            saved_chain = current_chain.id
            break

        chain_count += 1
    os.remove(temporary_pdb_file)
    io.save(temporary_pdb_file)
            
            ## Save the contents of the output file as a string
    with open(temporary_pdb_file, 'r') as saved_pdb:
        pdb_string = saved_pdb.read()
        saved_pdb.close()

    chains = structure.get_chains()
    chain_list = list(chains)
    num_chains = len(chain_list)

    first_residue_number = list(structure.get_residues())[0].id[1]
    if isinstance(first_residue_number, int):
        shift = int(first_residue_number) - 1
    else:
        shift = 0
            
    record_num = 0

            # Iterate through chain and select the appropriate sequence
    for record in SeqIO.parse(temporary_pdb_file, 'pdb-atom'):
        if record_num == 0:
            my_seq = record.seq
        if record.annotations['chain'] == chain:
            my_seq = record.seq

        record_num += 1
    return my_seq,shift,saved_chain,pdb_string

def read_pdb_file(pdb_file, chain):
    """
    Reads a PDB file and returns a PDBStructure object.

    Parameters
    ----------
    pdb_file : str
        The contents of the PDB file as a string.
    
    chain : str
        The name of the chain to extract

    Returns
    -------
    my_seq : str
        The sequence of the extracted chain.
    shift : int
        The shift in residue numbering required to match the PDB file.
    saved_chain : str
        The chain id of the saved chain.
    pdb_string : str
        The contents of the temporary PDB file as a string.

    Notes
    -----
    This function assumes that the PDB file contains a single chain. If the file contains multiple chains, the function will extract the first chain.
    """
    current_datetime = str(datetime.datetime.now())
    temporary_pdb_file = './static/molstar_plugin/plugin/dist/pdb_files/' + current_datetime + ".pdb"
    with open(temporary_pdb_file, 'w') as saved_pdb:
        saved_pdb.write(str(pdb_file).replace("\\n", "\n"))
        saved_pdb.close()

    io = PDBIO()
    structure = PDBParser().get_structure('structure', temporary_pdb_file)

    my_seq, shift, saved_chain, pdb_string = extract_chain(chain, temporary_pdb_file, io, structure)
    
    # Cleanup
    os.remove(temporary_pdb_file)

    return my_seq, shift, saved_chain, pdb_string


@app.route('/api/query', methods=['GET'])
def api_id():
    """This can be used for api calling {blobulator_link}/api/query?my_seq=AAAA&domain_threshold=24&cutoff=0.5&my_disorder=2,3"""
    my_seq  = str(request.args['my_seq'])
    hydro_scale = str(request.args['hydro_scale'])
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
    hydro_scale = request.form['hydro_scale']
    my_disorder  = request.form['my_disorder']
    my_disorder  = list(map(int, my_disorder.split(",")))
    window = 3
    my_initial_df = compute(
        str(my_seq),
        float(cutoff),
        float(domain_threshold),
        str(hydro_scale),
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
        hydro_scale = request.args['hydro_scale']
        domain_threshold  = request.args['domain_threshold']
        cutoff  = request.args['cutoff']
        my_disorder  = [0]
        window = 3
        fig = compute(
            str(my_seq),
            float(cutoff),
            hydro_scale,
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
    
@app.route("/PDB", methods=["GET", "POST"])
def analyze_pdb():
    pdb_string = request.form['pdb']
    chain = 'A'
    my_seq, shift, saved_chain, pdb_string = read_pdb_file(pdb_string, chain)
    return str(my_seq)

if __name__ == "__main__":
    app.run(debug=True)
