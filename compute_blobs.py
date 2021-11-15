import pandas as pd
import numpy as np
from amino_acids import (
    properties_charge,
    THREE_TO_ONE,
    properties_type,
    properties_hydropathy,
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
counter_p = 0  #
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
        return 0.3




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

#file = open("ncprCMap.pkl", "rb")
#ncprDict = pickle.load(file)
#file.close()
ncprDict = pd.read_csv("ncprCMap.csv", index_col=0)
def lookupNCPR(x):
    val = x[0]
    return ncprDict.loc[np.round(val, 2)]


#file = open("uverskyCMap.pkl", "rb")
#uverskyDict = pickle.load(file)
#file.close()
uverskyDict = pd.read_csv("uverskyCMap.csv", index_col=0)
def lookupUversky(x):
    val = x[0]
    return uverskyDict.loc[np.round(val, 2)]

#file = open("disorderCMap.pkl", "rb")
#disorderDict = pickle.load(file)
#file.close()
disorderDict = pd.read_csv("disorderCMap.csv", index_col=0)
def lookupDisorder(x):
    val = x[0]
    return disorderDict.loc[np.round(val, 2)]


#file = open("enrichCMap.pkl", "rb")
#enrichDF = pd.read_pickle(file)
#file.close()
enrichDF = pd.read_csv("enrichCMap.csv", index_col=[0,1])
def lookupEnrichment(x):
    cutoff = round(x[1], 2)
    blob_length = x[0]
    blob_type = x[2]
    #check if blob type is h AND the cutoff/bloblength combination exists in the reference set
    if blob_type == 'h':
        try:
            return enrichDF.color.loc[cutoff, blob_length]
        except KeyError:
            return "grey"
    else:
        return "grey"

def h_blob_enrichments_numerical(x):
    cutoff = round(x[1], 2)
    if x[2] == 'h':
        try:
            enrich_value = enrichDF[(cutoff, x[0])]
            return enrich_value
        except KeyError:
            return 0
    else:
        return 0

def count_var(x, v):
    return x.values.tolist().count(v) / (x.shape[0] * 1.0)

def domain_to_skyline_numbers(x):
    """convert domains to skyline height for javascript display"""
    if x[0][0] == "p":
        return 0.2
    elif x[0][0] == "h":
        return 0.6
    else:
        return 0.3

def compute(seq, cutoff, domain_threshold, window=3, disorder_residues=[]):

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
    df["hydropathy"] = [ properties_hydropathy[x] for x in df["seq_name"]] 
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
    df["domain"] = ['h' if (x >= domain_threshold and y == 1) else 't' if y==0  else 'p' for x, y in zip(df['domain_pre'], df["hydropathy_digitized"]) ]    
    df["domain_pre"] = (df["domain"].groupby(df["domain"].ne(df["domain"].shift()).cumsum()).transform("count"))  
    df["domain"] = ['t' if y=='t' else y if (x >= domain_threshold) else 's' for x, y in zip(df['domain_pre'], df["domain"]) ]
    df['blobtype'] = df['domain']

    df["domain_to_numbers"] = df[["domain", "hydropathy"]].apply(
        domain_to_numbers, axis=1)
    df["domain_for_skyline"] = df[["domain", "hydropathy"]].apply(
        domain_to_skyline_numbers, axis=1)


    # ..........................Define domain names.........................................................#
    df['domain'] =  df['domain'].groupby(df['domain'].ne(df['domain'].shift()).cumsum()).apply(lambda x: f3(x, domain_threshold))
    counts_group_length = df['domain'].value_counts().to_dict()#
    

    df['domain'] = df[['domain_pre', 'domain']].apply(lambda x: f4(x, domain_threshold, counts_group_length),axis=1)
    df['domain'].fillna(value='s', inplace=True)



    # ..........................Define the properties of each identified domain.........................................................#
    domain_group = df.groupby(["domain"])

    df["N"] = domain_group["resid"].transform("count")
    df["H"] = domain_group["hydropathy"].transform("mean")
    df["NCPR"] = domain_group["charge"].transform("mean")
    df["disorder"] = domain_group["disorder"].transform("mean")
    df["f+"] = domain_group["charge"].transform(lambda x: count_var(x, 1))
    df["f-"] = domain_group["charge"].transform(lambda x: count_var(x, -1))
    df["fcr"] = df["f-"] + df["f+"]
    df['h_blob_enrichment'] = df[["N", "m_cutoff", "blobtype"]].apply(lookupEnrichment, axis=1)
    df['h_numerical_enrichment'] = df[["N", "m_cutoff", "blobtype"]].apply(lambda x: h_blob_enrichments_numerical(x), axis=1)

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

def read_fasta(fname):
    
    if __name__ == "__main__":

    #For diagnostics/development benchmarking
    #import cProfile

    #seq = "MAQILPIRFQEHLQLQNLGINPANIGFSTLTMESDKFICIREKVGEQAQVVIIDMNDPSNPIRRPISADSAIMNPASKVIALKAGKTLQIFNIEMKSKMKAHTMTDDVTFWKWISLNTVALVTDNAVYHWSMEGESQPVKMFDRHSSLAGCQIINYRTDAKQKWLLLTGISAQQNRVVGAMQLYSVDRKVSQPIEGHAASFAQFKMEGNAEESTLFCFAVRGQAGGKLHIIEVGTPPTGNQPFPKKAVDVFFPPEAQNDFPVAMQISEKHDVVFLITKYGYIHLYDLETGTCIYMNRISGETIFVTAPHEATAGIIGVNRKGQVLSVCVEEENIIPYITNVLQNPDLALRMAVRNNLAGAEELFARKFNALFAQGNYSEAAKVAANAPKGILRTPDTIRRFQSVPAQPGQTSPLLQYFGILLDQGQLNKYESLELCRPVLQQGRKQLLEKWLKEDKLECSEELGDLVKSVDPTLALSVYLRANVPNKVIQCFAETGQVQKIVLYAKKVGYTPDWIFLLRNVMRISPDQGQQFAQMLVQDEEPLADITQIVDVFMEYNLIQQCTAFLLDALKNNRPSEGPLQTRLLEMNLMHAPQVADAILGNQMFTHYDRAHIAQLCEKAGLLQRALEHFTDLYDIKRAVVHTHLLNPEWLVNYFGSLSVEDSLECLRAMLSANIRQNLQICVQVASKYHEQLSTQSLIELFESFKSFEGLFYFLGSIVNFSQDPDVHFKYIQAACKTGQIKEVERICRESNCYDPERVKNFLKEAKLTDQLPLIIVCDRFDFVHDLVLYLYRNNLQKYIEIYVQKVNPSRLPVVIGGLLDVDCSEDVIKNLILVVRGQFSTDELVAEVEKRNRLKLLLPWLEARIHEGCEEPATHNALAKIYIDSNNNPERFLRENPYYDSRVVGKYCEKRDPHLACVAYERGQCDLELINVCNENSLFKSLSRYLVRRKDPELWGSVLLESNPYRRPLIDQVVQTALSETQDPEEVSVTVKAFMTADLPNELIELLEKIVLDNSVFSEHRNLQNLLILTAIKADRTRVMEYINRLDNYDAPDIANIAISNELFEEAFAIFRKFDVNTSAVQVLIEHIGNLDRAYEFAERCNEPAVWSQLAKAQLQKGMVKEAIDSYIKADDPSSYMEVVQAANTSGNWEELVKYLQMARKKARESYVETELIFALAKTNRLAELEEFINGPNNAHIQQVGDRCYDEKMYDAAKLLYNNVSNFGRLASTLVHLGEYQAAVDGARKANSTRTWKEVCFACVDGKEFRLAQMCGLHIVVHADELEELINYYQDRGYFEELITMLEAALGLERAHMGMFTELAILYSKFKPQKMREHLELFWSRVNIPKVLRAAEQAHLWAELVFLYDKYEEYDNAIITMMNHPTDAWKEGQFKDIITKVANVELYYRAIQFYLEFKPLLLNDLLMVLSPRLDHTRAVNYFSKVKQLPLVKPYLRSVQNHNNKSVNESLNNLFITEEDYQALRTSIDAYDNFDNISLAQRLEKHELIEFRRIAAYLFKGNNRWKQSVELCKKDSLYKDAMQYASESKDTELAEELLQWFLQEEKRECFGACLFTCYDLLRPDVVLETAWRHNIMDFAMPYFIQVMKEYLTKVDKLDASESLRKEEEQATETQPIVYGQPQLMLTAGPSVAVPPQAPFGYGYTAPPYGQPQPGFGYSM"
    #cProfile.run("compute(seq, 0.4, 4)")
    #for i in range(1,len(seq), 5):
     #   cProfile.run("compute(seq[0:i], 0.4, 4)")

    #df = compute("MSPQTETKASVGFKAGVKDYKLTYYTPEYETKDTDILAAFRVTPQPGVPPEEAGAAVAAESSTGTWTTVWTDGLTSLDRYKGRCYHIEPVAGEENQYICYVAYPLDLFEEGSVTNMFTSIVGNVFGFKALRALRLEDLRIPTAYVKTFQGPPHGIQVERDKLNKYGRPLLGCTIKPKLGLSAKNYGRAVYECLRGGLDFTKDDENVNSQPFMRWRDRFLFCAEAIYKSQAETGEIKGHYLNATAGTCEEMMKRAIFARELGVPIVMHDYLTGGFTANTSLAHYCRDNGLLLHIHRAMHAVIDRQKNHGIHFRVLAKALRMSGGDHIHSGTVVGKLEGERDITLGFVDLLRDDFIEKDRSRGIYFTQDWVSLPGVLPVASGGIHVWHMPALTEIFGDDSVLQFGGGTLGHPWGNAPGAVANRVALEACVQARNEGRDLAREGNEIIREACKWSPELAAACEVWKEIKFEFQAMDTL", 0.4, 1)
    

        df = compute("MSPQTETKASVGFKAGVKDYKLTYYTPEYETKDTDILAAFRVTPQPGVPPEEAGAAVAAESSTGTWTTVWTDGLTSLDRYKGRCYHIEPVAGEENQYICYVAYPLDLFEEGSVTNMFTSIVGNVFGFKALRALRLEDLRIPTAYVKTFQGPPHGIQVERDKLNKYGRPLLGCTIKPKLGLSAKNYGRAVYECLRGGLDFTKDDENVNSQPFMRWRDRFLFCAEAIYKSQAETGEIKGHYLNATAGTCEEMMKRAIFARELGVPIVMHDYLTGGFTANTSLAHYCRDNGLLLHIHRAMHAVIDRQKNHGIHFRVLAKALRMSGGDHIHSGTVVGKLEGERDITLGFVDLLRDDFIEKDRSRGIYFTQDWVSLPGVLPVASGGIHVWHMPALTEIFGDDSVLQFGGGTLGHPWGNAPGAVANRVALEACVQARNEGRDLAREGNEIIREACKWSPELAAACEVWKEIKFEFQAMDTL", 0.4, 4)
        df = df.rename(columns={'seq_name': 'res_name', 'm_cutoff': 'hydrophobicity_cutoff', 'domain_threshold':'minimum_blob_length', 'blobtype':'blob_hydrophobicty_class', 'N':'blob_length'})
        
        print ("Writing output file")
        df[['res_name', 'hydrophobicity_cutoff', 'minimum_blob_length', 'blob_hydrophobicty_class', 'blob_charge_class','blob_length']].to_csv("./blobulated.csv", index=False)
        print("done")
