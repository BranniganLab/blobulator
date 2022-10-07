import pandas as pd
import numpy as np
from amino_acids import (
    properties_charge,
    THREE_TO_ONE,
    properties_type,
    properties_hydropathy,
    properties_hydropathy_eisenberg_weiss,
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from random import random
import matplotlib.gridspec as gridspec
import math

import matplotlib as mpl
from matplotlib.lines import Line2D

import pickle

import os 
pd.options.mode.chained_assignment = 'raise'

# accessing the properties of the given sequence

counter_s = 0  # this is global variable used for annotating domains in f3
counter_p = 0  
counter_h = 0

s_counter = 0 # this is global variable used for annotating domains in f4


# character naming of domain names
ch = "a"
counter_domain_naming = ord(ch)


## COLOR MAPS
cmap = LinearSegmentedColormap.from_list(
    "mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")]
)

vmax=2.5
cmap_enrich = LinearSegmentedColormap.from_list('mycmap', [(0/ vmax, 'red'), (1./vmax, 'whitesmoke'), (vmax / vmax, 'blue')])

cNorm_enrich = matplotlib.colors.Normalize(vmin=0, vmax=2) #re-wrapping normalization
scalarMap_enrich = matplotlib.cm.ScalarMappable(norm=cNorm_enrich, cmap=cmap)

cmap_disorder = plt.get_cmap('PuOr')
cmap_u = plt.get_cmap('PuOr')
#This is when you want to change the scale of colormap
cNorm = matplotlib.colors.Normalize(vmin=-0.3, vmax=0.3) #re-wrapping normalization
scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap=cmap_u)
cval = scalarMap.to_rgba(0)

def domain_to_numbers(x):
    """convert domains to bar height for javascript display"""
    if x[0][0] == "p":
        return 0.2
    elif x[0][0] == "h":
        return 0.6
    else:
        return 0.4




# ..........................Define phase diagram.........................................................#
def phase_diagram(x):
    fcr = x[1]
    ncpr = x[0]
    fp = x[2]
    fn = x[3]

    # if we're in region 1
    if fcr < 0.25:
        return "rgb(138.0,251.0,69.0)"

        # if we're in region 2
    elif fcr >= 0.25 and fcr <= 0.35:
        return "rgb(254.0,230.0,90.0)"

        # if we're in region 3
    elif fcr > 0.35 and abs(ncpr) < 0.35:
        return "mediumorchid"

        # if we're in region 4 or 5
    elif fp > 0.35:
        if fn > 0.35:
            raise SequenceException(
                "Algorithm bug when coping with phase plot regions"
            )
        return "blue"

    elif fn > 0.35:
        return "red"

    else:  # This case is impossible but here for completeness\
        raise SequenceException(
            "Found inaccessible region of phase diagram. Numerical error"
        )


def phase_diagram_class(x):
    fcr = x[1]
    ncpr = x[0]
    fp = x[2]
    fn = x[3]

    # if we're in region 1
    if fcr < 0.25:
        return "1"

        # if we're in region 2
    elif fcr >= 0.25 and fcr <= 0.35:
        return "2"

        # if we're in region 3
    elif fcr > 0.35 and abs(ncpr) < 0.35:
        return "3"

        # if we're in region 4 or 5
    elif fp > 0.35:
        if fn > 0.35:
            raise SequenceException(
                "Algorithm bug when coping with phase plot regions"
            )
        return "5"

    elif fn > 0.35:
        return "4"

    else:  # This case is impossible but here for completeness\
        raise SequenceException(
            "Found inaccessible region of phase diagram. Numerical error"
        )


# ..........................Define colors for each blob type.........................................................#

def blob_diagram(x):
    """convert domains to colors for blob figure"""
    if x[0][0] == "p":
        return "#F7931E"
    elif x[0][0] == "h":
        return "#0071BC"
    else:
        return "#2DB11A"

# ..........................Define phase diagram.........................................................#
def uversky_diagram(x):
    h = x[1]*1.0
    ncpr = abs(x[0])
    c = 0.413 # intercept of diagram
    a = (1/2.785)
    b=-1
    distance = abs(a*ncpr + b*h +c)/math.sqrt(a**2+b**2)
    rel_line = h-(ncpr*a) - c
    if rel_line >= 0:
        return distance * -1.0
    else:
        return distance 

# ..........................Define NCPR.........................................................#
ncprDict = pd.read_csv("ncprCMap.csv", index_col=0)
def lookupNCPR(x):
    val = x[0]
    return ncprDict.loc[np.round(val, 2)]

uverskyDict = pd.read_csv("uverskyCMap.csv", index_col=0)
def lookupUversky(x):
    val = x[0]
    return uverskyDict.loc[np.round(val, 2)]

disorderDict = pd.read_csv("disorderCMap.csv", index_col=0)
def lookupDisorder(x):
    val = x[0]
    return disorderDict.loc[np.round(val, 2)]

enrichDF = pd.read_csv("enrichCMap.csv", index_col=[0,1])
enrichDF.to_csv("enrichment.txt")

def lookupEnrichment(x):
    min_hydrophobicity = round(x[1], 2)
    blob_length = x[0]
    blob_type = x[2]
    #check if blob type is h AND the cutoff/bloblength combination exists in the reference set
    if blob_type == 'h':
        try:
            return enrichDF.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    else:
        return "grey"

def h_blob_enrichments_numerical(x):
    cutoff = round(x[1], 2)
    if x[2] == 'h':
        try:
            enrich_value = enrichDF.Enrichment.loc[cutoff, x[0]]
            return enrich_value
        except KeyError:
            return 0
    else:
        return 0

def count_var(x, v):
    return x.values.tolist().count(v) / (x.shape[0] * 1.0)

def get_hydrophobicity(x, hydro_scale):
    if hydro_scale == "kyte_doolittle":
        scale = properties_hydropathy
    elif hydro_scale == "eisenberg_weiss":
        scale = properties_hydropathy_eisenberg_weiss
    try: 
        return scale[x]
    except:
        print(f'\n!!!ERROR: Residue {x} is not in my library of known amino acids!!!\n')
        raise

def clean_df(df):
    #print (df.head)
    #df = df.drop(range(0, 1))
    del df['domain_pre']
    del df['NCPR_color']
    del df['blob_color']
    del df["P_diagram"]
    del df["uversky_color"]
    del df["disorder_color"]
    del df["hydropathy_3_window_mean"] 
    del df["hydropathy_digitized"] 
    #del df["hydropathy"]
    del df["charge"]
    del df["domain_to_numbers"]
    df['resid'] = df['resid'].astype(int)
    df = df[[ 'resid', 'seq_name', 'window', 'm_cutoff', 'domain_threshold', 'N', 'H', 'min_h', 'blobtype', 'domain', 'blob_charge_class', 'NCPR', 'f+', 'f-', 'fcr', 'U_diagram', 'h_numerical_enrichment', 'disorder', 'hydropathy']]
    df = df.rename(columns={'seq_name': 'Residue_Name', 
                            'resid': 'Residue_Number', 
                            'disorder': 'Blob_Disorder', 
                            'window': 'Window', 
                            'm_cutoff': 'Hydropathy_Cutoff', 
                            'domain_threshold': 'Minimum_Blob_Length', 
                            'blobtype':'Blob_Type', 
                            'H': 'Normalized_Mean_Blob_Hydropathy',
                            'min_h': 'Min_Blob_Hydropathy', 
                            'domain': 'Blob_Index_Number', 
                            'NCPR': 'Blob_NCPR', 
                            'f+': "Fraction_of_Positively_Charged_Residues", 
                            'f-': "Fraction_of_Negatively_Charged_Residues", 
                            'fcr': 'Fraction_of_Charged_Residues', 
                            'h_numerical_enrichment': 'dSNP_enrichment', 
                            'blob_charge_class': 'Blob_Das-Pappu_Class', 
                            'U_diagram': 'Uversky_Diagram_Score', 
                            'hydropathy': 'Normalized_Kyte-Doolittle_hydropathy',
                            'N': 'blob_length'})
    df['Kyte-Doolittle_hydropathy'] = df['Normalized_Kyte-Doolittle_hydropathy']*9-4.5

    return df

def compute(seq, cutoff, domain_threshold, hydro_scale='kyte_doolittle', window=3, disorder_residues=[]):

    # give the numeric values to each domain
    def f3(x, domain_threshold):
        global counter_s
        global counter_p
        global counter_h
        if x.name == 1:
            counter_s=0  #intitialising the global value of counter to 0
            counter_p=0
            counter_h=0
            if x.iloc[0] == 'h':
                counter_h+=1
                return x + str(counter_h)
            elif x.iloc[0] == 'p':
                counter_p+=1
                return x + str(counter_p)
            else:
                counter_s+=1
                return x + str((counter_s))


        elif len(x) >= domain_threshold:
            if x.iloc[0] == 'h':
                counter_h+=1
                return x + str(counter_h)
            else:
                counter_p+=1
                return x + str(counter_p)
        else:
            counter_s+=1
            if counter_h>=1:
                counter_h=counter_h-1
                return x + str((counter_s))
            else:
                return x + str(counter_s)#


    # gives the alphabetic names to each domain
    def f4(x, domain_threshold, counts_group_length):
        global counter_domain_naming
        global s_counter
        if x[1][0] == 'p':
            counter_domain_naming = 0
            s_counter = 0
            return x[1]
        elif x[0] < domain_threshold:
            if x[1] == 's':
                counter_domain_naming = 0
                s_counter = 0
            else:
                s_counter = s_counter + 1
                if s_counter == x[0]:
                    counter_domain_naming = counter_domain_naming + 1
                    return x[1]
                else:
                    return x[1]
        else:
            if counts_group_length[x[1]] != x[0]:
                s_counter = 0
                return x[1] + chr(ord('a')+int(counter_domain_naming))
            else:
                s_counter = 0
                return x[1]#

    window_factor = int((window - 1) / 2)
    seq_start = 1  # starting resid for the seq
    resid_range = range(seq_start, len(seq) + 1 + seq_start)

    seq_name = []
    resid = []
    for i, j in zip(seq, resid_range):
        seq_name.append(str(i))
        resid.append(j)

    df = pd.DataFrame({"seq_name": seq_name, "resid": resid,})
    df["disorder"] = df["resid"].apply(lambda x: 1 if x in disorder_residues else 0 )
    df["hydropathy"] = [get_hydrophobicity(x, hydro_scale) for x in df["seq_name"]]
    df["charge"] = [properties_charge[x] for x in df["seq_name"]]           
    df["charge"] = df["charge"].astype('int')
    df["window"] = window
    df["m_cutoff"] = cutoff
    df["domain_threshold"] = domain_threshold

    #........................calcutes three residue moving window mean............................#
    df["hydropathy_3_window_mean"] = (df["hydropathy"].rolling(window=window, min_periods=0).mean())


    df["hydropathy_digitized"] = [ 1 if x > cutoff else 0 if np.isnan(x)  else -1 for x in df["hydropathy_3_window_mean"]]
    #define continous stretch of residues
    df["domain_pre"] = (df["hydropathy_digitized"].groupby(df["hydropathy_digitized"].ne(df["hydropathy_digitized"].shift()).cumsum()).transform("count"))
    df["hydropathy_digitized"] = [ 1 if x > cutoff else 0 if np.isnan(x)  else -1 for x in df["hydropathy_3_window_mean"]]    

    # ..........................Define domains.........................................................#
    df["domain"] = ['h' if (x >= domain_threshold and y == 1) else 't' if y==0  else 'p' for x, y in zip(df['domain_pre'], df["hydropathy_digitized"].astype(int)) ]    
    df["domain_pre"] = (df["domain"].groupby(df["domain"].ne(df["domain"].shift()).cumsum()).transform("count"))  
    df["domain"] = ['t' if y=='t' else y if (x >= domain_threshold) else 's' for x, y in zip(df['domain_pre'], df["domain"]) ]
    df['blobtype'] = df['domain']

    df["domain_to_numbers"] = df[["domain", "hydropathy"]].apply(
        domain_to_numbers, axis=1)

    # ..........................Define domain names.........................................................#
    df['domain'] =  df['domain'].groupby(df['domain'].ne(df['domain'].shift()).cumsum()).apply(lambda x: f3(x, domain_threshold))
    counts_group_length = df['domain'].value_counts().to_dict()#
    

    df['domain'] = df[['domain_pre', 'domain']].apply(lambda x: f4(x, domain_threshold, counts_group_length),axis=1)
    df['domain'].fillna(value='s', inplace=True)



    # ..........................Define the properties of each identified domain.........................................................#
    domain_group = df.groupby(["domain"])

    df["N"] = domain_group["resid"].transform("count")
    df["H"] = domain_group["hydropathy"].transform("mean")
    df["min_h"] = domain_group["hydropathy"].transform("min")
    df["NCPR"] = domain_group["charge"].transform("mean")
    df["disorder"] = domain_group["disorder"].transform("mean")
    df["f+"] = domain_group["charge"].transform(lambda x: count_var(x, 1))
    df["f-"] = domain_group["charge"].transform(lambda x: count_var(x, -1))
    df["fcr"] = df["f-"] + df["f+"]
    df['h_blob_enrichment'] = df[["N", "min_h", "blobtype"]].apply(lookupEnrichment, axis=1)
    df['h_numerical_enrichment'] = df[["N", "min_h", "blobtype"]].apply(lambda x: h_blob_enrichments_numerical(x), axis=1)

    df["blob_color"] = df[["domain", "hydropathy"]].apply(
        blob_diagram, axis=1)
    df["P_diagram"] = df[["NCPR", "fcr", "f+", "f-"]].apply(
        phase_diagram, axis=1
    )
    df["blob_charge_class"] = df[["NCPR", "fcr", "f+", "f-"]].apply(
        phase_diagram_class, axis=1
    )
    df["U_diagram"] = df[["NCPR", "H"]].apply(
        uversky_diagram, axis=1
    )
    df["NCPR_color"] = df[["NCPR", "fcr"]].apply(
        lookupNCPR, axis=1
    )
    df["uversky_color"] = df[["U_diagram", "fcr"]].apply(
        lookupUversky, axis=1
    )

    df["disorder_color"] = df[["disorder", "fcr"]].apply(
        lookupDisorder, axis=1
    )

    return df

if __name__ == "__main__":

    import argparse
    from Bio import SeqIO
    from Bio.Seq import Seq

    #For diagnostics/development benchmarking
    #import cProfile

    #seq = "MAQILPIRFQEHLQLQNLGINPANIGFSTLTMESDKFICIREKVGEQAQVVIIDMNDPSNPIRRPISADSAIMNPASKVIALKAGKTLQIFNIEMKSKMKAHTMTDDVTFWKWISLNTVALVTDNAVYHWSMEGESQPVKMFDRHSSLAGCQIINYRTDAKQKWLLLTGISAQQNRVVGAMQLYSVDRKVSQPIEGHAASFAQFKMEGNAEESTLFCFAVRGQAGGKLHIIEVGTPPTGNQPFPKKAVDVFFPPEAQNDFPVAMQISEKHDVVFLITKYGYIHLYDLETGTCIYMNRISGETIFVTAPHEATAGIIGVNRKGQVLSVCVEEENIIPYITNVLQNPDLALRMAVRNNLAGAEELFARKFNALFAQGNYSEAAKVAANAPKGILRTPDTIRRFQSVPAQPGQTSPLLQYFGILLDQGQLNKYESLELCRPVLQQGRKQLLEKWLKEDKLECSEELGDLVKSVDPTLALSVYLRANVPNKVIQCFAETGQVQKIVLYAKKVGYTPDWIFLLRNVMRISPDQGQQFAQMLVQDEEPLADITQIVDVFMEYNLIQQCTAFLLDALKNNRPSEGPLQTRLLEMNLMHAPQVADAILGNQMFTHYDRAHIAQLCEKAGLLQRALEHFTDLYDIKRAVVHTHLLNPEWLVNYFGSLSVEDSLECLRAMLSANIRQNLQICVQVASKYHEQLSTQSLIELFESFKSFEGLFYFLGSIVNFSQDPDVHFKYIQAACKTGQIKEVERICRESNCYDPERVKNFLKEAKLTDQLPLIIVCDRFDFVHDLVLYLYRNNLQKYIEIYVQKVNPSRLPVVIGGLLDVDCSEDVIKNLILVVRGQFSTDELVAEVEKRNRLKLLLPWLEARIHEGCEEPATHNALAKIYIDSNNNPERFLRENPYYDSRVVGKYCEKRDPHLACVAYERGQCDLELINVCNENSLFKSLSRYLVRRKDPELWGSVLLESNPYRRPLIDQVVQTALSETQDPEEVSVTVKAFMTADLPNELIELLEKIVLDNSVFSEHRNLQNLLILTAIKADRTRVMEYINRLDNYDAPDIANIAISNELFEEAFAIFRKFDVNTSAVQVLIEHIGNLDRAYEFAERCNEPAVWSQLAKAQLQKGMVKEAIDSYIKADDPSSYMEVVQAANTSGNWEELVKYLQMARKKARESYVETELIFALAKTNRLAELEEFINGPNNAHIQQVGDRCYDEKMYDAAKLLYNNVSNFGRLASTLVHLGEYQAAVDGARKANSTRTWKEVCFACVDGKEFRLAQMCGLHIVVHADELEELINYYQDRGYFEELITMLEAALGLERAHMGMFTELAILYSKFKPQKMREHLELFWSRVNIPKVLRAAEQAHLWAELVFLYDKYEEYDNAIITMMNHPTDAWKEGQFKDIITKVANVELYYRAIQFYLEFKPLLLNDLLMVLSPRLDHTRAVNYFSKVKQLPLVKPYLRSVQNHNNKSVNESLNNLFITEEDYQALRTSIDAYDNFDNISLAQRLEKHELIEFRRIAAYLFKGNNRWKQSVELCKKDSLYKDAMQYASESKDTELAEELLQWFLQEEKRECFGACLFTCYDLLRPDVVLETAWRHNIMDFAMPYFIQVMKEYLTKVDKLDASESLRKEEEQATETQPIVYGQPQLMLTAGPSVAVPPQAPFGYGYTAPPYGQPQPGFGYSM"
    #cProfile.run("compute(seq, 0.4, 4)")
    #for i in range(1,len(seq), 5):
     #   cProfile.run("compute(seq[0:i], 0.4, 4)")

    #df = compute("MSPQTETKASVGFKAGVKDYKLTYYTPEYETKDTDILAAFRVTPQPGVPPEEAGAAVAAESSTGTWTTVWTDGLTSLDRYKGRCYHIEPVAGEENQYICYVAYPLDLFEEGSVTNMFTSIVGNVFGFKALRALRLEDLRIPTAYVKTFQGPPHGIQVERDKLNKYGRPLLGCTIKPKLGLSAKNYGRAVYECLRGGLDFTKDDENVNSQPFMRWRDRFLFCAEAIYKSQAETGEIKGHYLNATAGTCEEMMKRAIFARELGVPIVMHDYLTGGFTANTSLAHYCRDNGLLLHIHRAMHAVIDRQKNHGIHFRVLAKALRMSGGDHIHSGTVVGKLEGERDITLGFVDLLRDDFIEKDRSRGIYFTQDWVSLPGVLPVASGGIHVWHMPALTEIFGDDSVLQFGGGTLGHPWGNAPGAVANRVALEACVQARNEGRDLAREGNEIIREACKWSPELAAACEVWKEIKFEFQAMDTL", 0.4, 1)
    
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--sequence', type=str, help='Takes a single string of EITHER DNA or protein one-letter codes (no spaces).', default=None)
    parser.add_argument('--cutoff', type=float, help='Sets the cutoff hydrophobicity (floating point number between 0.00 and 1.00 inclusive). Defaults to 0.4', default=0.4)
    parser.add_argument('--minBlob', type=int, help='Mininmum blob length (integer greater than 1). Defaults to 4', default=4)
    parser.add_argument('--oname', type=str, help='Name of output file or path to output directory. Defaults to blobulated_.csv', default="blobulated_")
    parser.add_argument('--fasta', type=str, help='FASTA file with 1 or more sequences', default=None)
    parser.add_argument('--DNA', type=bool, help='Flag that says whether the inputs are DNA or protein. Defaults to false (protein)', default=False)

    args = parser.parse_args()

    if args.DNA:
        print("REMINDER: The blobulator assumes all DNA inputs to be coding sequences and only translates up to the first stop codon.")
        print("CAUTION: Do not mix DNA and protein sequences")
    if (args.sequence!=None) & (args.fasta!=None):
        print("ERROR: Input EITHER --sequence OR --fasta. NOT both.")

    elif args.fasta:
        print(f"Reading {args.fasta}")
        for seq_record in SeqIO.parse(args.fasta, "fasta"):
            print(f'Running: {seq_record.id}')
            if args.DNA:
                coding_dna = seq_record.seq
                mrna = coding_dna.transcribe()
                sequence = mrna.translate(to_stop=True)
            else:
                sequence = seq_record.seq
            df = compute(sequence, args.cutoff, args.minBlob, 'kyte_doolittle')
            print(f"Writing output file to: {args.oname}{seq_record.id}.csv")
            df = clean_df(df)
            df.to_csv(f'{args.oname}{seq_record.id}.csv', index=False)

    elif args.sequence:
        print(f'Running...\nseq: {args.sequence}\ncutoff: {args.cutoff}\nminBlob: {args.minBlob}\nOutput to: {args.oname}')
        if args.DNA:
            coding_dna = Seq(args.sequence)
            mrna = coding_dna.transcribe()
            sequence = mrna.translate(to_stop=True)
        else:
            sequence = args.sequence
        
        df = compute(sequence, args.cutoff, args.minBlob, 'kyte_doolittle')
        print ("Writing output file")
        df = clean_df(df)
        df.to_csv(args.oname, index=False)

        print("done")
    else:
        print("No sequence provided")

