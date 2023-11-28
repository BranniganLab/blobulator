import pandas as pd
import numpy as np
from .amino_acids import (
    properties_charge,
    THREE_TO_ONE,
    properties_type,
    properties_hydropathy,
    properties_hydropathy_eisenberg_weiss,
)

from importlib.resources import files

blob_path = files("blobulator").joinpath("data")

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
    """
    A function that assigns heights to each residue for output tracks based on what type of blob they fall into

    Arguments:
        x (array): An array containing the the type of blob that each residue falls into

    Returns:
        int: height for each residue

    """
    if x[0][0] == "p":
        return 0.2
    elif x[0][0] == "h":
        return 0.6
    else:
        return 0.4




# ..........................Define phase diagram.........................................................#
def phase_diagram(x):
    """
    A function that assigns colors to blobs based on their Das-Pappu class

    Arguments:
        x (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        color (str): the rgb value for each residue bar based on its Das-Pappu class
    """

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
    """
    A function to assign numerical values to blobs based on their Das-Pappu class

    Arguments:
        x (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        region (str): returns the number associated to the Das-Pappu class for each residue
    """

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
    """
    A function that colors blobs based on their blob types

    Arguments:
        x (array): An array containing the the type of blob that each residue falls into

    Returns:
        color (str): color for each residue based on its blob type
    """
    if x[0][0] == "p":
        return "#F7931E"
    elif x[0][0] == "h":
        return "#0071BC"
    else:
        return "#2DB11A"

# ..........................Define phase diagram.........................................................#
def uversky_diagram(x):
    """
    A function that calculates the distance from the disorder/order boundary for each blob on the uversky diagram

    Arguments:
        x (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        distance (int): the distance of each blob from the from the disorder/order boundary on the uversky diagram
    """
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

def lookupNCPR(x):

    """
    A function that returns the color for each blob based on its NCPR

    Arguments:
        x (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        color (str): a string containing the color value for each residue based on the ncpr of the blob that it's contained in
    """
    import matplotlib
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")])

    norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=0.2)
    
    fraction = np.round(x[0], 2)
    
    returned_rgb = matplotlib.colors.to_rgba(cmap(norm(fraction)))
    return "rgb(" + str(returned_rgb[0] * 255) + "," + str(returned_rgb[1] * 255) + "," + str(returned_rgb[2] * 255) + ")"


fname = blob_path.joinpath("uverskyCMap.csv")
uverskyDict = pd.read_csv(fname, index_col=0)
def lookupUversky(x):
    """
    A function that returns the color for each blob based on its distance from the disorder/order boundary for on the uversky diagram

    Arguments:
        x (array): An array containing the uversky distances for each residue by blob

    Returns:
        color (str): a string containing the color value for each residue based on the distance from the uversky diagram's disorder/order boundary line of the blob that it's contained in
    """

    val = x[0]
    return uverskyDict.loc[np.round(val, 2)]

fname = blob_path.joinpath("disorderCMap.csv")
disorderDict = pd.read_csv(fname, index_col=0)
def lookupDisorder(x):
    """
    A function that returns the color for each blob based on how disordered it is, determined by the Uniprot accession

    Arguments:
        x (array): An array containing the disorder value for each residue by blob

    Returns:
        color (str): a string containing the color value for each residue based on how disordered the blob that contains it is predicted to be
    """
    val = x[0]
    return disorderDict.loc[np.round(val, 2)]

fname = blob_path.joinpath("enrichCMap.csv")
enrichDF = pd.read_csv(fname, index_col=[0, 1])
#enrichDF.to_csv("../data/enrichment.txt")

fname = blob_path.joinpath("enrichCMap_p.csv")
enrichDF_p = pd.read_csv(fname, index_col=[0, 1])
#enrichDF_p.to_csv("../data/enrichment_p.txt")

fname = blob_path.joinpath("enrichCMap_s.csv")
enrichDF_s = pd.read_csv(fname, index_col=[0, 1])
#enrichDF_s.to_csv("../data/enrichment_s.txt")

def lookupEnrichment(x):
    """
    A function that returns the color for each blob based on how sensitive to mutation it is predicted to be.
    Note: this function requires the minimum smoothed hydropathy for each blob. The analysis from Lohia et al. 2022 that produced the data by which blobs are colored involved increasing the H* threshold, and the minimum smoothed hydropathy is what determines that any given h-blob of a given length is still considered an h-blob as this threshold is increased.
    
    Arguments:
        x (array): An array containing the number of residues in the blob, the minimum smoothed hydropathy, and the type of blob it is

    Returns:
        color (str): a string containing the color value for each residue based on sensitive to mutation the blob that contains it is estimated to be
    """
    
    min_hydrophobicity = round(x[1], 2)
    blob_length = x[0]
    blob_type = x[2]
    #check if blob type is h AND the cutoff/bloblength combination exists in the reference set
    if blob_type == 'h':
        try:
            return enrichDF.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    elif blob_type == 'p':
        try:
            return enrichDF_p.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    elif blob_type == 's':
        try:
            return enrichDF_s.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    else:
        return "grey"

def h_blob_enrichments_numerical(x):
    """
    A function that returns the color for each h-blob based on how sensitive to mutation it is predicted to be

    Arguments:
        x (array): An array containing the predicted mutation sensitivity value for each residue for each h-blob

    Returns:
        color (str): a string containing the color value for each residue based on sensitive to mutation the blob that contains it is estimated to be, if it's an h-blob
    """
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
    """
    A counting function

    Arguments:
        x (array): An array containing the predicted mutation sensitivity value for each residue by blob
        v (int): how many to count

    Returns:
        int: the total count for each value
    """
    return x.values.tolist().count(v) / (x.shape[0] * 1.0)

def get_hydrophobicity(x, hydro_scale):
    """
    A function that returns the hydrophobicity per residue based on which scale the user has selected

    Arguments:
        x (array): An array containing the predicted mutation sensitivity value for each residue by blob
        hydro_scale (str): the hydrophobicity scale as selected by the user

    Returns:
        hydrophobicity (int): the hydrophobicity for a given residue in the selected scale
    """
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
    """
    A function removes unnecessary columns from a given dataframe

    Arguments:
        df (dataframe): A pandas dataframe

    Returns:
        df (dataframe): A cleaned pandas dataframe
    """
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
    """
    A function that runs the blobulation algorithm

    Arguments:
        seq (str): A sequence of amino acids
        cutoff (float): the user-selected cutoff
        domain_threshold (int): the minimum length cutoff
        hydro_scale (str): the selected hydrophobicity scale
        window (int): the smoothing window for calculating residue hydrophobicity
        disorder_residues (list): known disorder values for each residue

    Returns:
        df (dataframe): A dataframe containing the output from blobulation
    """

    def f3(x, domain_threshold):
        """
        A function that gives the numeric values to each set of residues comprising the blobs
        
        Arguments: 
            x (array): An array containing the blob types of each residue
            domain_threshold (int): minimum length (L_min) provided by the user

        Returns:
            Digitized sequence of str giving the length of each given blob

        """
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
                return x + str(counter_s)


    def f4(x, domain_threshold, counts_group_length):
        """
        A function that gives the alphabetic names to each set of residues comprising the blobs
 
        Arguments: 
            x (array): An array containing the blob types of each residue
            domain_threshold (int): minimum length (L_min) provided by the user
            counts_group_length (int): the length of each given blob in the sequence

        Returns:
            Digitized sequence of str outlining the blobs

        """
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

    def calculate_smoothed_hydropathy(hydropath):
        """Calculates the smoothed hydropathy of a given residue with its two ajacent neighbors
            
            Arguments:
                hydropath(int): The hydropathy for a given residue

            NOTE: This function makes sue of the center=True pandas rolling argument to ensure the residue in question is at the center of smoothing calculation
            It is important to run the regression test to check that the smoothed hydropathy is expected (see github Wiki/Regression Checklist for instructions on how to perform this test."""
        smoothed_hydropath = hydropath.rolling(window=3, min_periods=0, center=True).mean()
        return smoothed_hydropath

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
    df["hydropathy_3_window_mean"] = calculate_smoothed_hydropathy(df["hydropathy"])
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
    df['domain'] =  df['domain'].groupby(df['domain'].ne(df['domain'].shift()).cumsum(), group_keys=False).apply(lambda x: f3(x, domain_threshold))
    counts_group_length = df['domain'].value_counts().to_dict()#
    

    df['domain'] = df[['domain_pre', 'domain']].apply(lambda x: f4(x, domain_threshold, counts_group_length),axis=1)
    df['domain'].fillna(value='s', inplace=True)



    # ..........................Define the properties of each identified domain.........................................................#
    domain_group = df.groupby(["domain"])

    df["N"] = domain_group["resid"].transform("count")
    df["H"] = domain_group["hydropathy"].transform("mean")
    df["min_h"] = domain_group["hydropathy_3_window_mean"].transform("min")
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


