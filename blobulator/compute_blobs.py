import pandas as pd
import numpy as np
from .amino_acids import (
    properties_charge,
    THREE_TO_ONE,
    properties_type,
    properties_hydropathy,
    properties_hydropathy_eisenberg_weiss,
    properties_hydropathy_moon_fleming,
)

from importlib.resources import files

blobulator_path = files("blobulator").joinpath("data")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from random import random
import matplotlib.gridspec as gridspec
import math

import matplotlib as mpl
from matplotlib.lines import Line2D

import pickle

import os 
pd.options.mode.chained_assignment = "raise"

counter_s = 0  
counter_p = 0  
counter_h = 0
s_counter = 0

# Character naming of blob_type names
ch = "a"
counter_blob_type_naming = ord(ch)

# Color map properties
cmap = LinearSegmentedColormap.from_list(
    "mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")]
)

vmax=2.5
cmap_enrich = LinearSegmentedColormap.from_list("mycmap", [(0/ vmax, "red"), (1./vmax, "whitesmoke"), (vmax / vmax, "blue")])

c_norm_enrich = matplotlib.colors.Normalize(vmin=0, vmax=2)
scalar_map_enrich = matplotlib.cm.ScalarMappable(norm=c_norm_enrich, cmap=cmap)

cmap_uversky = plt.get_cmap("PuOr")
cmap_disorder = plt.get_cmap("PuOr")

c_norm = matplotlib.colors.Normalize(vmin=-0.3, vmax=0.3) 
scalarMap = matplotlib.cm.ScalarMappable(norm=c_norm, cmap=cmap_uversky)
cval = scalarMap.to_rgba(0)

from string import ascii_lowercase 

def divmod_base26(n):
    """
    A modified version of the divmod() function that returns the quotient and remainder of an integer divided by 26, but with the special case where the remainder is 0 returning the quotient minus 1 and the remainder plus 26.

    This is used to convert a number into base 26 using the lowercase English alphabet.

    Arguments:
    n (int): The number to convert into base 26

    Returns:
    tuple: A tuple containing the quotient and remainder of the given number divided by 26, with the special case handling.
    """
    a, b = divmod(n, 26)                                                        
    if b == 0:
        return a - 1, b + 26
    return a, b

def to_base26(num):
    """
    Converts a given number into base 26 using the lowercase English alphabet.

    Arguments:
    num (int): The number to convert into base 26

    Returns
    str: The base 26 representation of the given number
    """
    chars = []
    while num > 0:                                                                                                                           
        num, d = divmod_base26(num)
        chars.append(ascii_lowercase[d - 1])
    return "".join(reversed(chars))

def name_blobs(res_types):
    """
    Reads the type of blob a residue classifies in (h, p, or s) and names the blob (e.g. h1a, h1b, p1, h2a, h2b etc...)
    
    Arguments:
        res_type (array): The blob type (h, p, or s) that each residue is classified in
    
    Returns:
        grouped_names (array): The names of all blobs in the sequence
    """
    h_counter = 0
    s_counter = 0
    p_counter = 0

    preliminary_names = []
    group_nums = []
    
    i = 0
    previous_residue = ""
    
    for residue in res_types:
        if residue == "h":
            if previous_residue == "":
                h_counter += 1
            preliminary_names.append(residue + str(h_counter))
    
        elif residue == "p":
            if previous_residue == "p":
                pass
            else:
                h_counter += 1
                p_counter += 1
            preliminary_names.append(residue + str(p_counter))
            
        else:
            if previous_residue == "s":
                pass
            else:
                s_counter += 1
            group_nums.append(h_counter)
            preliminary_names.append(residue + str(s_counter))
        
        previous_residue = residue
        i += 1
        
    grouped_names = []
    
    i = 1
    previous_residue = ""
    for item in preliminary_names:
        if item[0] == "h" and (int(item[1:]) in group_nums):
            item += to_base26(i)
        elif item[0] == "s" and previous_residue != "s":
            i += 1
        if item[0] == "p":
            i = 1
        previous_residue = item[0]
        grouped_names.append(item)
    
    return grouped_names
        
def assign_residue_track_bar_height(blob_properties_array):
    """
    Assigns bar heights to each residue for output tracks based on what type of blob they fall into

    Arguments:
        blob_properties_array (array): An array containing the the type of blob that each residue falls into

    Returns:
        int: bar height for each residue
    """
    if blob_properties_array.iloc[0][0] == "p":
        return 0.2
    elif blob_properties_array.iloc[0][0] == "h":
        return 0.6
    else:
        return 0.4

# ..........................Define phase diagram................................................#
def assign_blob_das_pappu_color(blob_properties_array):
    """
    Assigns colors to blobs based on where they lie in the Das-Pappu phase diagram: (Fig 7) https://www.pnas.org/doi/10.1073/pnas.1304749110

    Arguments:
        blob_properties_array (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        color (str): The rgb value for each residue bar based on its Das-Pappu class
    """
    fraction_of_charged_residues = blob_properties_array.iloc[1]
    ncpr = blob_properties_array.iloc[0]
    fraction_of_positively_charged_residues = blob_properties_array.iloc[2]
    fraction_of_negatively_charged_residues = blob_properties_array.iloc[3]

    # If blob is in region 1 of das pappu diagram
    if fraction_of_charged_residues < 0.25:
        return "rgb(138.0,251.0,69.0)"

    # If blob is in region 2 of das pappu diagram
    elif fraction_of_charged_residues >= 0.25 and fraction_of_charged_residues <= 0.35:
        return "rgb(254.0,230.0,90.0)"

    # If blob is in region 3 of das pappu diagram
    elif fraction_of_charged_residues > 0.35 and abs(ncpr) < 0.35:
        return "mediumorchid"

    # If blob is in region 5 of das pappu diagram
    elif fraction_of_positively_charged_residues > 0.35:
        if fraction_of_negatively_charged_residues > 0.35:
            raise SequenceException(
                "Algorithm bug when coping with phase plot regions"
            )
        return "blue"
    
    # If blob is in region 4 of das pappu diagram    
    elif fraction_of_negatively_charged_residues > 0.35:
        return "red"

    else:  # This case is impossible but here for completeness
        raise SequenceException(
            "Found inaccessible region of phase diagram. Numerical error"
        )

def assign_blob_das_pappu_value(blob_properties_array):
    """
    Assigns numerical values to blobs based on where they lie in the Das-Pappu phase diagram: (Fig 7) https://www.pnas.org/doi/10.1073/pnas.1304749110

    Arguments:
        blob_properties_array (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        region (str): returns the number associated to the Das-Pappu class for each residue
    """
    fraction_of_charged_residues = blob_properties_array.iloc[1]
    ncpr = blob_properties_array.iloc[0]
    fraction_of_positively_charged_residues = blob_properties_array.iloc[2]
    fraction_of_negatively_charged_residues = blob_properties_array.iloc[3]

    # If blob is in region 1 of das pappu diagram
    if fraction_of_charged_residues < 0.25:
        return "1"

    # If blob is in region 2 of das pappu diagram
    elif fraction_of_charged_residues >= 0.25 and fraction_of_charged_residues <= 0.35:
        return "2"

    # If blob is in region 3 of das pappu diagram
    elif fraction_of_charged_residues > 0.35 and abs(ncpr) < 0.35:
        return "3"

    # If blob is in region 5 of das pappu diagram
    elif fraction_of_positively_charged_residues > 0.35:
        if fraction_of_negatively_charged_residues > 0.35:
            raise SequenceException(
                "Algorithm bug when coping with phase plot regions"
            )
        return "5"

    # If blob is in region 4 of das pappu diagram
    elif fraction_of_negatively_charged_residues > 0.35:
        return "4"

    else:  # This case is impossible but here for completeness
        raise SequenceException(
            "Found inaccessible region of phase diagram. Numerical error"
        )

# ..........................Define colors for each blob type....................................#
def assign_blob_color_by_type(blob_properties_array):
    """
    Determines the color for blobs based on their blob types

    Arguments:
        blob_properties_array (array): An array containing the the type of blob that each residue falls into

    Returns:
        color (str): Color for each residue based on its blob type
    """
    if blob_properties_array.iloc[0][0] == "p":
        return "#F7931E"
    elif blob_properties_array.iloc[0][0] == "h":
        return "#0071BC"
    else:
        return "#2DB11A"

# ..........................Define phase diagram................................................#
def assign_blob_uversky_value(blob_properties_array):
    """
    Calculates the distance (uversky value)from the disorder/order boundary for each blob on the uversky diagram

    Arguments:
        blob_properties_array (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        distance (int): The distance of each blob from the from the disorder/order boundary on the uversky diagram
    """
    h = blob_properties_array.iloc[1]*1.0
    ncpr = abs(blob_properties_array.iloc[0])
    c = 0.413 # intercept of diagram
    a = (1/2.785)
    b=-1
    distance = abs(a*ncpr + b*h +c)/math.sqrt(a**2+b**2)
    rel_line = h-(ncpr*a) - c
    if rel_line >= 0:
        return distance * -1.0 ## multiplied by -1 for colorscale assignment
    else:
        return distance 

# ..........................Define NCPR.........................................................#
def assign_blob_ncpr_color(blob_properties_array):
    """
    Assigns the color for each blob based on its NCPR

    Arguments:
        blob_properties_array (array): An array containing the fraction of positive and negative residues per blob

    Returns:
        color (str): String containing the color value for each residue based on the NCPR of the blob that it's contained in
    """
    import matplotlib
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")])

    norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=0.2)
    
    fraction = np.round(blob_properties_array.iloc[0], 2)
    
    returned_rgb = matplotlib.colors.to_rgba(cmap(norm(fraction)))
    return "rgb(" + str(returned_rgb[0] * 255) + "," + str(returned_rgb[1] * 255) + "," + str(returned_rgb[2] * 255) + ")"

fname = blobulator_path.joinpath("uverskyCMap.csv")
uverskyDict = pd.read_csv(fname, index_col=0)

def assign_blob_uversky_color(blob_properties_array):
    """
    Assigns the color for each blob based on its distance from the disorder/order boundary on the Uversky diagram

    Arguments:
        blob_properties_array (array): An array containing the uversky distances for each residue by blob

    Returns:
        color (str): a string containing the color value for each residue based on the distance from the uversky diagram"s disorder/order boundary line of the blob that it's contained in
    """
    val = blob_properties_array.iloc[0]
    return uverskyDict.loc[np.round(val, 2)]

fname = blobulator_path.joinpath("disorderCMap.csv")
disorderDict = pd.read_csv(fname, index_col=0)

def assign_blob_disorder_color(blob_properties_array):
    """
    Assigns the color value for each blob based on how disordered it is which is determined by the Uniprot accession

    Arguments:
        blob_properties_array (array): An array containing the disorder value for each residue by blob

    Returns:
        color (str): String containing the color value for each residue based on how disordered the blob that contains it is predicted to be
    """
    val = blob_properties_array.iloc[0]
    return disorderDict.loc[np.round(val, 2)]

fname = blobulator_path.joinpath("enrichCMap.csv")
enrich_df = pd.read_csv(fname, index_col=[0, 1])
#enrich_df.to_csv("../data/enrichment.txt")

fname = blobulator_path.joinpath("enrichCMap_p.csv")
enrich_df_p = pd.read_csv(fname, index_col=[0, 1])
#enrich_df_p.to_csv("../data/enrichment_p.txt")

fname = blobulator_path.joinpath("enrichCMap_s.csv")
enrich_df_s = pd.read_csv(fname, index_col=[0, 1])
#enrich_df_s.to_csv("../data/enrichment_s.txt")

def assign_blob_predicted_dsnp_enrichment_color(blob_properties_array):
    """
    Assigns the color for each blob based on how sensitive to mutation it is predicted to be.
    Note: This function requires the minimum smoothed hydropathy for each blob. The analysis from 
        Lohia et al. 2022 that produced the data by which blobs are colored involved increasing the H* 
        threshold, and the minimum smoothed hydropathy is what determines that any given h-blob of a 
        given length is still considered an h-blob as this threshold is increased.
    
    Arguments:
        blob_properties_array (array): An array containing the number of residues in the blob, the minimum smoothed hydropathy, and the type of blob it is

    Returns:
        color (str): String containing the color value for each residue based on sensitive to mutation the blob that contains it is predicted to be
    """
    min_hydrophobicity = round(blob_properties_array.iloc[1], 2)
    blob_length = blob_properties_array.iloc[0]
    residue_blob_type = blob_properties_array.iloc[2]

    if residue_blob_type == "h":
        try:
            return enrich_df.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    elif residue_blob_type == "p":
        try:
            return enrich_df_p.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    elif residue_blob_type == "s":
        try:
            return enrich_df_s.color.loc[min_hydrophobicity, blob_length]
        except KeyError:
            return "grey"
    else:
        return "grey"

def assign_blob_predicted_dsnp_enrichment_value(blob_properties_array):
    """
    Assigns the color for each h-blob in a given sequence based on how sensitive to a mutation it is predicted to be

    Arguments:
        blob_properties_array (array): An array containing the predicted mutation sensitivity value for each residue for each h-blob

    Returns:
        color (str): String containing the color value for each residue based on how sensitive to a mutation the blob that contains it is predicted to be
    """
    cutoff = round(blob_properties_array.iloc[1], 2)
    if blob_properties_array.iloc[2] == "h":
        try:
            enrich_value = enrich_df.Enrichment.loc[cutoff, blob_properties_array.iloc[0]]
            return enrich_value
        except KeyError:
            return 0
    else:
        return 0

def count_var(blob_properties_array, v):
    """
    Counts the number of times v appears in an array

    Arguments:
        blob_properties_array (array): An array containing various properties organized by blob
        v (int): How many to count

    Returns:
        int: The total count for each value
    """
    return blob_properties_array.values.tolist().count(v) / (blob_properties_array.shape[0] * 1.0)

def get_hydrophobicity(residue, hydropathy_scale):
    """
    Reads the string of the user-defined hydropathy scale and retrieves the scale's properties

    Arguments:
        residue (str): A given residue's amino acid type
        hydropathy_scale (str): The hydrophobicity scale as selected by the user

    Returns:
        hydrophobicity (int): The hydrophobicity for a given residue in the selected scale
    """
    if hydropathy_scale == "kyte_doolittle":
        scale = properties_hydropathy
    elif hydropathy_scale == "eisenberg_weiss":
        scale = properties_hydropathy_eisenberg_weiss
    elif hydropathy_scale == "moon_fleming":
        scale = properties_hydropathy_moon_fleming
    try: 
        return scale[residue]
    except:
        print(f"\n!!!ERROR: Residue {residue} is not in my library of known amino acids!!!\n")
        raise

def clean_df(df):
    """
    Removes unnecessary columns from a given dataframe

    Arguments:
        df (dataframe): A pandas dataframe

    Returns:
        df (dataframe): A cleaned pandas dataframe
    """
    #print (df.head)
    #df = df.drop(range(0, 1))
    del df["residue_blob_type_pre"]
    del df["color_for_NCPR_track"]
    del df["color_for_blobtype_track"]
    del df["color_for_daspappu_track"]
    del df["color_for_uversky_track"]
    del df["color_for_disorder_predictor_track"]
    del df["hydropathy_digitized"]
    del df["residue_charge"]
    # del df["assign_residue_track_bar_height"]
    del df["residue_disorder"]
    df["residue_number"] = df["residue_number"].astype(int)
    df = df[[ "residue_number",
             "residue_name",
             "smoothing_window_length",
             "hydropathy_cutoff",
             "blob_length_minimum",
             "blob_length",
             "blob_hydrophobicity",
             "blob_minimum_hydrophobicity",
             "residue_blob_type",
             "residue_blob_groups",
             "blob_daspappu_phase",
             "blob_net_charge_per_residue",
             "blob_fraction_of_positively_charged_residues",
             "blob_fraction_of_negatively_charged_residues",
             "blob_fraction_of_charged_residues",
             "blob_distance_from_uversky_boundary_line",
             "blob_predicted_enrichment_of_dsnps",
             "blob_disorder",
             "residue_hydropathy",
             "residue_smoothed_hydropathy"]]
    df = df.rename(columns={"residue_name": "Residue_Name",
                            "residue_number": "Residue_Number", 
                            "blob_disorder": "Blob_Disorder", 
                            "smoothing_window_length": "Window", 
                            "hydropathy_cutoff": "Hydropathy_Cutoff", 
                            "blob_length_minimum": "Minimum_Blob_Length", 
                            "residue_blob_type":"Blob_Type", 
                            "blob_hydrophobicity": "Normalized_Mean_Blob_Hydropathy",
                            "blob_minimum_hydrophobicity": "Min_Blob_Hydropathy", 
                            "residue_blob_groups": "Blob_Index_Number", 
                            "blob_net_charge_per_residue": "Blob_NCPR", 
                            "blob_fraction_of_positively_charged_residues": "Fraction_of_Positively_Charged_Residues", 
                            "blob_fraction_of_negatively_charged_residues": "Fraction_of_Negatively_Charged_Residues", 
                            "blob_fraction_of_charged_residues": "Fraction_of_Charged_Residues", 
                            "blob_predicted_enrichment_of_dsnps": "dSNP_enrichment", 
                            "blob_daspappu_phase": "Blob_Das-Pappu_Class", 
                            "blob_distance_from_uversky_boundary_line": "Uversky_Diagram_Score", 
                            "residue_hydropathy": "Normalized_hydropathy",
                            "residue_smoothed_hydropathy": "Smoothed_Hydropathy",
                            "blob_length": "blob_length"})
    #df["Kyte-Doolittle_hydropathy"] = df["Normalized_Kyte-Doolittle_hydropathy"]*9-4.5

    return df

def calculate_smoothed_hydropathy(residue, smoothing_window_length):
    """
    Calculates the smoothed hydropathy of a given residue with its two ajacent neighbors.
    
    Arguments:
        residue (pandas.Series): The series of hydropathy values
        smoothing_window_length (int): The number of residues to consider when calculating the smoothed hydropathy (Lmin)
     
    Returns:
        residue_smoothed_hydropathy (pandas.Series): The smoothed hydropathy of the given residue
        
    Notes:
    This function makes sure of the center=True pandas rolling argument to ensure the 
    residue in question is at the center of smoothing calculation
    It is important to run the regression test to check that the smoothed hydropathy is 
    expected (see github Wiki/Regression Checklist for instructions on how to perform 
    this test.
    """
    residue_smoothed_hydropathy = residue.rolling(smoothing_window_length, min_periods=0, center=True).mean()

    return residue_smoothed_hydropathy

def build_sequence_df(seq, disorder_residues=[], hydropathy_scale="kyte_doolittle"):
    """
    This function takes a protein sequence and creates a pandas DataFrame with the
    following columns:
        - residue_number: 1-indexed position of each residue
        - residue_name: Single-letter amino acid code
        - residue_disorder: 1 if the residue is disordered, else 0
        - residue_hydropathy: Hydropathy value from the chosen scale
        - residue_charge: Integer charge of the residue

    Arguments:
        seq (str): The amino acid sequence of a protein.
        disorder_residues (list of int, optional): List of residue numbers (1-indexed) that are considered disordered. Defaults to an empty list.
        hydropathy_scale (str, optional): Name of the hydropathy scale to use (e.g., "kyte_doolittle"). Defaults to "kyte_doolittle".

    Returns:
        df (pd.DataFrame): A dataframe with the above columns.
    """
    residue_number = list(range(1, len(seq)+1))
    residue_name = list(seq)

    df = pd.DataFrame({
        "residue_number": residue_number,
        "residue_name": residue_name
    })

    df["residue_disorder"] = df["residue_number"].apply(lambda x: 1 if x in disorder_residues else 0)
    df["residue_hydropathy"] = [get_hydrophobicity(r, hydropathy_scale) for r in df["residue_name"]]
    df["residue_charge"] = [properties_charge[r] for r in df["residue_name"]]
    df["residue_charge"] = df["residue_charge"].astype(int)

    return df

def smooth_and_digitize(df, hydropathy_cutoff, smoothing_window_length=3):
    """
    Compute smoothed hydropathy and digitized hydropathy for blob assignment.

    Smoothed hydropathy is the average of the hydropathy values over a window of
    length `smoothing_window_length`. The digitized hydropathy is then assigned as
    follows:
        - hydrophobic: 1 if smoothed hydropathy > `hydropathy_cutoff`
        - neutral: 0 if smoothed hydropathy is NaN
        - hydrophilic: -1 if smoothed hydropathy < `hydropathy_cutoff`

    Arguments:
        df (pd.DataFrame): DataFrame containing at least a column 'residue_hydropathy'.
        hydropathy_cutoff (float): Threshold for classifying residues as hydrophobic (>cutoff), neutral (NaN), or hydrophilic (<cutoff).
        smoothing_window_length (int, optional): Window length for smoothing hydropathy values. Default is 3.

    Returns:
        pd.DataFrame: The original DataFrame with two new columns:
                        - 'residue_smoothed_hydropathy': hydropathy values smoothed over the window.
                        - 'hydropathy_digitized': residues coded as 1 (hydrophobic), 0 (neutral/NaN), or -1 (hydrophilic) based on smoothed hydropathy.
    """
    df["residue_smoothed_hydropathy"] = calculate_smoothed_hydropathy(df["residue_hydropathy"], smoothing_window_length)
    df["hydropathy_digitized"] = [1 if x > hydropathy_cutoff else 0 if np.isnan(x) else -1 
                                  for x in df["residue_smoothed_hydropathy"]]
    return df

def assign_blob_types(df, blob_length_minimum):
    """
    Assign preliminary blob types ('h','p','t','s') and name blobs.

    We use three rules to assign blob types to each residue in the sequence:

    1. If the residue is hydrophobic and part of a stretch of hydrophobic residues
       of length >= blob_length_minimum, the blob type is 'h'.
    2. If the residue is neutral, the blob type is 't'.
    3. If the residue is hydrophilic and part of a stretch of hydrophilic residues
       of length >= blob_length_minimum, the blob type is 'p'.
    4. If the residue is hydrophilic and part of a stretch of hydrophilic residues
       of length < blob_length_minimum, the blob type is 's'.

    After assigning the blob types, we name each blob with a number. The number
    is determined by the order of the blobs in the sequence.

    Arguments:
        df (pd.DataFrame): DataFrame containing a column 'hydropathy_digitized' with the digitized hydropathy values.
        blob_length_minimum (int): Minimum length of a blob to be considered a blob.

    Returns:
        df (pd.DataFrame): The original DataFrame with the following new columns:
                            - 'residue_blob_type': blob type ('h', 'p', 't', 's')
                            - 'residue_blob_groups': blob number (1, 2, 3, etc.)
    """
    df["residue_blob_type_pre"] = (df["hydropathy_digitized"].groupby(df["hydropathy_digitized"].ne(df["hydropathy_digitized"].shift()).cumsum()).transform("count"))
    df["residue_blob_type"] = ["h" if (x >= blob_length_minimum and y == 1) else "t" if y==0 else "p"
                               for x, y in zip(df["residue_blob_type_pre"], df["hydropathy_digitized"].astype(int))]
    df["residue_blob_type_pre"] = (df["residue_blob_type"].groupby(df["residue_blob_type"].ne(df["residue_blob_type"].shift()).cumsum()).transform("count"))
    df["residue_blob_type"] = ["t" if y=="t" else y if (x >= blob_length_minimum) else "s"
                               for x, y in zip(df["residue_blob_type_pre"], df["residue_blob_type"])]
    df["assign_residue_track_bar_height"] = df[["residue_blob_type", "residue_hydropathy"]].apply(assign_residue_track_bar_height, axis=1)
    df["residue_blob_groups"] = pd.Series(name_blobs(df["residue_blob_type"].to_list()))
    df.fillna({"residue_blob_groups": "s"}, inplace=True)

    return df

def compute_blob_properties(df):
    """
    Compute blob-level properties like length, hydropathy, NCPR, fraction charged, enrichment, etc.

    This function takes a DataFrame with a column 'residue_blob_groups' and computes
    the following blob-level properties:

    - blob_length: the length of the blob
    - blob_hydrophobicity: the mean hydropathy of the blob
    - blob_minimum_hydrophobicity: the minimum smoothed hydropathy of the blob
    - blob_net_charge_per_residue: the mean net charge per residue of the blob
    - blob_disorder: the mean disorder probability of the blob
    - blob_fraction_of_positively_charged_residues: the fraction of positively charged residues in the blob
    - blob_fraction_of_negatively_charged_residues: the fraction of negatively charged residues in the blob
    - blob_fraction_of_charged_residues: the fraction of charged residues in the blob
    - blob_predicted_enrichment_of_dsnps: the predicted enrichment of dsnp in the blob
    - blob_daspappu_phase: the Das-Pappu phase of the blob
    - blob_distance_from_uversky_boundary_line: the distance of the blob from the Uversky boundary line

    The blob-level properties are computed by grouping the DataFrame by 'residue_blob_groups'
    and applying the corresponding functions to the groups.

    Arguments:
        df (pd.DataFrame): DataFrame containing a column 'residue_blob_groups'

    Returns:
        df (pd.DataFrame): The original DataFrame with the additional columns
    """
    blobs = df.groupby(["residue_blob_groups"])
    df["blob_length"] = blobs["residue_number"].transform("count")
    df["blob_hydrophobicity"] = blobs["residue_hydropathy"].transform("mean")
    df["blob_minimum_hydrophobicity"] = blobs["residue_smoothed_hydropathy"].transform("min")
    df["blob_net_charge_per_residue"] = blobs["residue_charge"].transform("mean")
    df["blob_disorder"] = blobs["residue_disorder"].transform("mean")
    df["blob_fraction_of_positively_charged_residues"] = blobs["residue_charge"].transform(lambda x: count_var(x, 1))
    df["blob_fraction_of_negatively_charged_residues"] = blobs["residue_charge"].transform(lambda x: count_var(x, -1))
    df["blob_fraction_of_charged_residues"] = df["blob_fraction_of_positively_charged_residues"] + df["blob_fraction_of_negatively_charged_residues"]
    df["blob_predicted_enrichment_of_dsnps"] = df[["blob_length", "blob_minimum_hydrophobicity", "residue_blob_type"]].apply(lambda x: assign_blob_predicted_dsnp_enrichment_value(x), axis=1)
    df["blob_daspappu_phase"] = df[["blob_net_charge_per_residue", "blob_fraction_of_charged_residues","blob_fraction_of_positively_charged_residues", "blob_fraction_of_negatively_charged_residues"]].apply(assign_blob_das_pappu_value, axis=1)
    df["blob_distance_from_uversky_boundary_line"] = df[["blob_net_charge_per_residue", "blob_hydrophobicity"]].apply(assign_blob_uversky_value, axis=1)
    return df

def assign_colors(df, color_types=None):
    """
    Assign colors for each track. color_types is a list of which color tracks to compute.

    This function assigns colors for each track based on the blob properties. The
    colors are assigned in the following order:

    - blobtype track: color based on the blob type
    - dsnp_enrichment track: color based on the predicted enrichment of dsnp
    - daspappu track: color based on the daspappu phase
    - NCPR track: color based on the net charge per residue
    - uversky track: color based on the distance from the uversky boundary line
    - disorder track: color based on the disorder probability

    The colors are stored in the following columns:

    - color_for_blobtype_track
    - color_for_dsnp_enrichment_track
    - color_for_daspappu_track
    - color_for_NCPR_track
    - color_for_uversky_track
    - color_for_disorder_predictor_track

    Arguments:
        df (pandas.DataFrame): The dataframe to assign colors to.
        color_types (list of str, optional): A list of which color tracks to compute. Defaults to all tracks.

    Returns:
        df (pandas.DataFrame): The dataframe with the assigned colors.
    """
    if color_types is None:
        color_types = ["blobtype", "dsnp_enrichment", "daspappu", "NCPR", "uversky", "disorder"]

    if "blobtype" in color_types:
        df["color_for_blobtype_track"] = df[["residue_blob_type", "residue_hydropathy"]].apply(assign_blob_color_by_type, axis=1)
    if "dsnp_enrichment" in color_types:
        df["color_for_dsnp_enrichment_track"] = df[["blob_length", "blob_minimum_hydrophobicity", "residue_blob_type"]].apply(assign_blob_predicted_dsnp_enrichment_color, axis=1)
    if "daspappu" in color_types:
        df["color_for_daspappu_track"] = df[["blob_net_charge_per_residue", "blob_fraction_of_charged_residues",
                                            "blob_fraction_of_positively_charged_residues", "blob_fraction_of_negatively_charged_residues"]].apply(
                                                assign_blob_das_pappu_color, axis=1)
    if "NCPR" in color_types:
        df["color_for_NCPR_track"] = df[["blob_net_charge_per_residue", "blob_fraction_of_charged_residues"]].apply(assign_blob_ncpr_color, axis=1)
    if "uversky" in color_types:
        df["color_for_uversky_track"] = df[["blob_distance_from_uversky_boundary_line", "blob_fraction_of_charged_residues"]].apply(assign_blob_uversky_color, axis=1)
    if "disorder" in color_types:
        df["color_for_disorder_predictor_track"] = df[["blob_disorder", "blob_fraction_of_charged_residues"]].apply(assign_blob_disorder_color, axis=1)

    return df

# Wrapper function to build entire data frame
def compute(seq, hydropathy_cutoff, blob_length_minimum, hydropathy_scale="kyte_doolittle", smoothing_window_length=3, disorder_residues=None, include_colors=True, color_types=None):
    """
    Wrapper function that runs all steps. Returns a full dataframe identical to original compute().

    This function takes a protein sequence and returns a pandas DataFrame with the following columns:
        - residue_number: 1-indexed position of each residue
        - residue_name: Single-letter amino acid code
        - residue_disorder: 1 if the residue is disordered, else 0
        - residue_hydropathy: Hydropathy value from the chosen scale
        - residue_charge: Integer charge of the residue
        - residue_blob_type: The type of blob the residue is in
        - blob_length: Length of the blob the residue is in
        - blob_hydrophobicity: Average hydropathy of the blob the residue is in
        - blob_net_charge_per_residue: Net charge of the blob the residue is in
        - blob_fraction_of_charged_residues: Fraction of charged residues in the blob the residue is in
        - blob_fraction_of_positively_charged_residues: Fraction of positively charged residues in the blob the residue is in
        - blob_fraction_of_negatively_charged_residues: Fraction of negatively charged residues in the blob the residue is in
        - blob_distance_from_uversky_boundary_line: Distance from the Uversky boundary line for the blob the residue is in
        - blob_minimum_hydrophobicity: Minimum hydropathy of the blob the residue is in
        - blob_predicted_enrichment_of_dsnps: Predicted enrichment of dsnp in the blob the residue is in
        - blob_daspappu_phase: Das-Pappu phase of the blob the residue is in
        - blob_disorder: Disorder probability of the blob the residue is in

    Arguments:
        seq (str): The amino acid sequence of a protein.
        hydropathy_cutoff (float): The cutoff below which a residue is considered hydrophobic.
        blob_length_minimum (int): The minimum length of a blob.
        hydropathy_scale (str, optional): The name of the hydropathy scale to use (e.g., "kyte_doolittle"). Defaults to "kyte_doolittle".
        smoothing_window_length (int, optional): The number of residues to consider when calculating the smoothed hydropathy (Lmin). Defaults to 3.
        disorder_residues (list of int, optional): List of residue numbers (1-indexed) that are considered disordered. Defaults to an empty list.
        include_colors (bool, optional): Whether to include color information in the output. Defaults to True.
        color_types (list of str, optional): A list of which color tracks to compute. Defaults to all tracks.

    Returns:
        df (pandas.DataFrame): A dataframe with the above columns.
    """
    if disorder_residues is None:
        disorder_residues = []

    # Build initial dataframe
    df = build_sequence_df(seq, disorder_residues, hydropathy_scale)

    # Smooth and digitize hydropathy
    df = smooth_and_digitize(df, hydropathy_cutoff, smoothing_window_length)

    # Assign blob types
    df = assign_blob_types(df, blob_length_minimum)

    # Compute blob properties
    df = compute_blob_properties(df)

    # Assign colors
    if include_colors:
        df = assign_colors(df, color_types)

    # Add data to columns
    df["smoothing_window_length"] = smoothing_window_length
    df["hydropathy_cutoff"] = hydropathy_cutoff
    df["blob_length_minimum"] = blob_length_minimum
    df["hydropathy_scale"] = hydropathy_scale
    df["disorder_residues"] = [disorder_residues] * len(df)
    return df
