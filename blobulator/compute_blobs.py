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
from string import ascii_lowercase 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from random import choices, random
import matplotlib.gridspec as gridspec
import math
import matplotlib as mpl
from matplotlib.lines import Line2D

pd.options.mode.chained_assignment = "raise"
blobulator_path = files("blobulator").joinpath("data")

counter_s = 0  
counter_p = 0  
counter_h = 0
s_counter = 0

# Character naming of blob_type names
ch = "a"
counter_blob_type_naming = ord(ch)

# Color map properties
cmap = LinearSegmentedColormap.from_list("mycmap", [(0.0 / 1, "red"), ((0.5) / 1, "whitesmoke"), (1.0, "blue")])

vmax=2.5
cmap_enrich = LinearSegmentedColormap.from_list("mycmap", [(0/ vmax, "red"), (1./vmax, "whitesmoke"), (vmax / vmax, "blue")])

c_norm_enrich = matplotlib.colors.Normalize(vmin=0, vmax=2)
scalar_map_enrich = matplotlib.cm.ScalarMappable(norm=c_norm_enrich, cmap=cmap)

cmap_uversky = plt.get_cmap("PuOr")
cmap_disorder = plt.get_cmap("PuOr")

c_norm = matplotlib.colors.Normalize(vmin=-0.3, vmax=0.3) 
scalarMap = matplotlib.cm.ScalarMappable(norm=c_norm, cmap=cmap_uversky)
cval = scalarMap.to_rgba(0)

cmap_ncpr = LinearSegmentedColormap.from_list("mycmap", ["red", "whitesmoke", "blue"])
norm = matplotlib.colors.Normalize(vmin=-0.2, vmax=0.2)

# Load dataframes for coloring blobs
fname_enrich_map = blobulator_path.joinpath("enrichCMap.csv")
enrich_df = pd.read_csv(fname_enrich_map, index_col=[0, 1])
#enrich_df.to_csv("../data/enrichment.txt")

fname_enrich_map_p = blobulator_path.joinpath("enrichCMap_p.csv")
enrich_df_p = pd.read_csv(fname_enrich_map_p, index_col=[0, 1])
#enrich_df_p.to_csv("../data/enrichment_p.txt")

fname_enrich_map_s = blobulator_path.joinpath("enrichCMap_s.csv")
enrich_df_s = pd.read_csv(fname_enrich_map_s, index_col=[0, 1])
#enrich_df_s.to_csv("../data/enrichment_s.txt")

fname_disorder_map = blobulator_path.joinpath("disorderCMap.csv")
disorderDict = pd.read_csv(fname_disorder_map, index_col=0).squeeze("columns")

fname_uversky_map = blobulator_path.joinpath("uverskyCMap.csv")
uverskyDict = pd.read_csv(fname_uversky_map, index_col=0).squeeze("columns")

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

def count_var(blob_properties_df, v):
    """
    Counts the number of times v appears in an array

    Arguments:
        blob_properties_df (array): An array containing various properties organized by blob
        v (int): How many to count

    Returns:
        int: The total count for each value
    """
    return blob_properties_df.values.tolist().count(v) / (blob_properties_df.shape[0] * 1.0)

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
        blob_properties_df (pd.DataFrame): A dataframe with the above columns.
    """
    residue_number = list(range(1, len(seq)+1))
    residue_name = list(seq)

    blob_properties_df = pd.DataFrame({
        "residue_number": residue_number,
        "residue_name": residue_name
    })

    blob_properties_df["residue_disorder"] = blob_properties_df["residue_number"].isin(disorder_residues).astype(int)
    blob_properties_df["residue_hydropathy"] = [get_hydrophobicity(r, hydropathy_scale) for r in blob_properties_df["residue_name"]]
    blob_properties_df["residue_charge"] = [properties_charge[r] for r in blob_properties_df["residue_name"]]
    blob_properties_df["residue_charge"] = blob_properties_df["residue_charge"].astype(int)

    return blob_properties_df

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

def smooth_and_digitize(blob_properties_df, hydropathy_cutoff, smoothing_window_length=3):
    """
    Compute smoothed hydropathy and digitized hydropathy for blob assignment.

    Smoothed hydropathy is the average of the hydropathy values over a window of
    length `smoothing_window_length`. The digitized hydropathy is then assigned as
    follows:
        - hydrophobic: 1 if smoothed hydropathy > `hydropathy_cutoff`
        - neutral: 0 if smoothed hydropathy is NaN
        - hydrophilic: -1 if smoothed hydropathy < `hydropathy_cutoff`

    Arguments:
        blob_properties_df (pd.DataFrame): DataFrame containing at least a column 'residue_hydropathy'.
        hydropathy_cutoff (float): Threshold for classifying residues as hydrophobic (>cutoff), neutral (NaN), or hydrophilic (<cutoff).
        smoothing_window_length (int, optional): Window length for smoothing hydropathy values. Default is 3.

    Returns:
        pd.DataFrame: The original DataFrame with two new columns:
                        - 'residue_smoothed_hydropathy': hydropathy values smoothed over the window.
                        - 'hydropathy_digitized': residues coded as 1 (hydrophobic), 0 (neutral/NaN), or -1 (hydrophilic) based on smoothed hydropathy.
    """
    blob_properties_df["residue_smoothed_hydropathy"] = calculate_smoothed_hydropathy(blob_properties_df["residue_hydropathy"], smoothing_window_length)
    blob_properties_df["hydropathy_digitized"] = [1 if x > hydropathy_cutoff else 0 if np.isnan(x) else -1 
                                                     for x in blob_properties_df["residue_smoothed_hydropathy"]]
    return blob_properties_df

def assign_residue_track_bar_height(blob_properties_df):
    """
    Assigns bar heights to each residue for output tracks based on what the blob type (p, h, or s)

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the type of blob (h, p, or s) that each residue falls into

    Returns:
        int: bar height for each residue
    """
    blob_types = blob_properties_df["residue_blob_type"].values.astype(str)
    
    # Get the first character of the blob type (e.g. 'p' for 'p1', 'h' for 'h1a', 's' for 's1'
    first_character = np.char.add(blob_types, "")
    first_character = np.array([s[0] for s in blob_types]) 

    # If p-blob return 0.2, if h-blob return 0.6, else (s-blob)return 0.4
    return np.select([first_character == "p", first_character == "h"], [0.2, 0.6], default=0.4)

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

def assign_blob_types(blob_properties_df, blob_length_minimum):
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
        blob_properties_df (pd.DataFrame): DataFrame containing a column 'hydropathy_digitized' with the digitized hydropathy values.
        blob_length_minimum (int): Minimum length of a blob to be considered a blob.

    Returns:
        blob_properties_df (pd.DataFrame): The original DataFrame with the following new columns:
                                            - 'residue_blob_type': blob type ('h', 'p', 't', 's')
                            - 'residue_blob_groups': blob number (1, 2, 3, etc.)
    """
    blob_properties_df["residue_blob_type_pre"] = (blob_properties_df["hydropathy_digitized"].groupby(blob_properties_df["hydropathy_digitized"].ne(blob_properties_df["hydropathy_digitized"].shift()).cumsum()).transform("count"))
    blob_properties_df["residue_blob_type"] = ["h" if (x >= blob_length_minimum and y == 1) else "t" if y==0 else "p"
                                               for x, y in zip(blob_properties_df["residue_blob_type_pre"], blob_properties_df["hydropathy_digitized"].astype(int))]
    blob_properties_df["residue_blob_type_pre"] = (blob_properties_df["residue_blob_type"].groupby(blob_properties_df["residue_blob_type"].ne(blob_properties_df["residue_blob_type"].shift()).cumsum()).transform("count"))
    blob_properties_df["residue_blob_type"] = ["t" if y=="t" else y if (x >= blob_length_minimum) else "s"
                                               for x, y in zip(blob_properties_df["residue_blob_type_pre"], blob_properties_df["residue_blob_type"])]
    blob_properties_df["assign_residue_track_bar_height"] = assign_residue_track_bar_height(blob_properties_df)
    blob_properties_df["residue_blob_groups"] = pd.Series(name_blobs(blob_properties_df["residue_blob_type"].to_list()))
    blob_properties_df.fillna({"residue_blob_groups": "s"}, inplace=True)

    return blob_properties_df

def assign_blob_das_pappu_value(blob_properties_df):
    """
    Assigns numerical values to blobs based on where they lie in the Das-Pappu phase diagram: (Fig 7) https://www.pnas.org/doi/10.1073/pnas.1304749110

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the fraction of positive and negative residues per blob

    Returns:
        blob_properties_df (pd.DataFrame): Returns a dataframe containing a column called "blob_daspappu_phase" containing the number associated to the Das-Pappu class/region for each residue
    """
    f_charged = blob_properties_df["blob_fraction_of_charged_residues"]
    ncpr = blob_properties_df["blob_net_charge_per_residue"].abs()
    f_pos = blob_properties_df["blob_fraction_of_positively_charged_residues"]
    f_neg = blob_properties_df["blob_fraction_of_negatively_charged_residues"]

    conditions = [
        (f_charged < 0.25),                                # Region 1
        (f_charged >= 0.25) & (f_charged <= 0.35),         # Region 2
        (f_charged > 0.35) & (ncpr < 0.35),                # Region 3
        (f_pos > 0.35),                                    # Region 5
        (f_neg > 0.35)                                     # Region 4
    ]

    regions = ["1", "2", "3", "5", "4"]

    blob_properties_df["blob_daspappu_phase"] = np.select(conditions, regions, default="Error")

    # This case is impossible but here for completeness
    if (blob_properties_df["blob_daspappu_phase"] == "Error").any():
         raise Exception("Found inaccessible region of phase diagram. Numerical error")

    return blob_properties_df

def assign_blob_predicted_dsnp_enrichment_value(blob_properties_df):
    """
    Assigns the enrichment value (color) for each h-blob in a given sequence based on how sensitive the sequence is predicted to be to a mutation.

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the predicted mutation sensitivity value for each residue for each h-blob

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing the predicted mutation sensitivity value for each residue for each h-blob in a column called "blob_predicted_enrichment_of_dsnps"
    """
    lookup_keys = list(zip(blob_properties_df["blob_minimum_hydrophobicity"].round(2), blob_properties_df["blob_length"]))
    blob_properties_df["blob_predicted_enrichment_of_dsnps"] = (enrich_df["Enrichment"].reindex(lookup_keys).fillna(0).values)
    blob_properties_df.loc[blob_properties_df["residue_blob_type"] != "h", "blob_predicted_enrichment_of_dsnps"] = 0
    
    return blob_properties_df

def assign_blob_uversky_value(blob_properties_df):
    """
    Calculates the distance (uversky value)from the disorder/order boundary for each blob on the uversky diagram

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the fraction of positive and negative residues per blob

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing a column called "blob_distance_from_uversky_boundary_line" containing the distance of each blob from the from the disorder/order boundary on the uversky diagram
    """
    hydrophobicity = blob_properties_df["blob_hydrophobicity"]
    ncpr = blob_properties_df["blob_net_charge_per_residue"].abs()
    
    # CONSTANTS
    c = 0.413 # intercept of diagram
    a = (1/2.785)
    b=-1
    
    distance = abs(a * ncpr + b * hydrophobicity + c) / math.sqrt(a**2 + b**2)
    rel_line = hydrophobicity - (ncpr * a) - c

    blob_properties_df["blob_distance_from_uversky_boundary_line"] = np.where(rel_line >= 0, distance * -1.0, distance)
    
    return blob_properties_df 

def compute_blob_properties(blob_properties_df):
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
        blob_properties_df (pd.DataFrame): DataFrame containing a column 'residue_blob_groups'

    Returns:
        blob_properties_df (pd.DataFrame): The original DataFrame with the additional columns
    """
    blobs = blob_properties_df.groupby(["residue_blob_groups"])
    blob_properties_df["blob_length"] = blobs["residue_number"].transform("count")
    blob_properties_df["blob_hydrophobicity"] = blobs["residue_hydropathy"].transform("mean")
    blob_properties_df["blob_minimum_hydrophobicity"] = blobs["residue_smoothed_hydropathy"].transform("min")
    blob_properties_df["blob_net_charge_per_residue"] = blobs["residue_charge"].transform("mean")
    blob_properties_df["blob_disorder"] = blobs["residue_disorder"].transform("mean")
    blob_properties_df["blob_fraction_of_positively_charged_residues"] = blobs["residue_charge"].transform(lambda x: count_var(x, 1))
    blob_properties_df["blob_fraction_of_negatively_charged_residues"] = blobs["residue_charge"].transform(lambda x: count_var(x, -1))
    blob_properties_df["blob_fraction_of_charged_residues"] = blob_properties_df["blob_fraction_of_positively_charged_residues"] + blob_properties_df["blob_fraction_of_negatively_charged_residues"]
    blob_properties_df = assign_blob_das_pappu_value(blob_properties_df)
    blob_properties_df = assign_blob_predicted_dsnp_enrichment_value(blob_properties_df)
    blob_properties_df = assign_blob_uversky_value(blob_properties_df)
    return blob_properties_df

def assign_blob_color_by_type(blob_properties_df):
    """
    Determines the color for blobs based on their blob types

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the type of blob (h, p, or s) that each residue falls into

    Returns:
        blob_properties_df (pd.DataFrame): Returns a dataframe containing a column called "color_for_blobtype_track" which holds the blob color that a residue is assigned
    """
    residue_blob_type = blob_properties_df["residue_blob_type"]

    conditions = [
        (residue_blob_type == "p"),
        (residue_blob_type == "h"),
    ]

    color_choices = ["#F7931E", "#0071BC"]

    blob_properties_df["color_for_blobtype_track"] = np.select(conditions, color_choices, default="#2DB11A")

    return blob_properties_df

def assign_blob_ncpr_color(blob_properties_df):
    """
    Assigns the color for each blob based on its NCPR

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the fraction of positive and negative residues per blob

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing a column called "color_for_NCPR_track" containing the color associated to the NCPR value for each residue based on the blob that it is contained in
    """
    ncpr = blob_properties_df["blob_net_charge_per_residue"].values
    ncpr = np.round(ncpr, 2)
    
    rgba_array = cmap_ncpr(norm(ncpr))

    r = (rgba_array[:, 0] * 255).astype(int).astype(str)
    g = (rgba_array[:, 1] * 255).astype(int).astype(str)
    b = (rgba_array[:, 2] * 255).astype(int).astype(str)
    
    blob_properties_df["color_for_NCPR_track"] = [f"rgb({ri},{gi},{bi})" for ri, gi, bi in zip(r, g, b)]

    return blob_properties_df

def assign_blob_das_pappu_color(blob_properties_df):
    """
    Assigns colors to blobs based on where they lie in the Das-Pappu phase diagram: (Fig 7) https://www.pnas.org/doi/10.1073/pnas.1304749110

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the fraction of positive and negative residues per blob

    Returns:
        blob_properties_df (pd.DataFrame): Returns a dataframe containing a column called "color_for_daspappu_track" containing the color associated to the Das-Pappu class/region for each residue.
    """
    fraction_of_charged_residues = blob_properties_df["blob_fraction_of_charged_residues"]
    ncpr = blob_properties_df["blob_net_charge_per_residue"].abs()
    fraction_of_positively_charged_residues = blob_properties_df["blob_fraction_of_positively_charged_residues"]
    fraction_of_negatively_charged_residues = blob_properties_df["blob_fraction_of_negatively_charged_residues"]

    conditions = [
        (fraction_of_charged_residues < 0.25),                                # Region 1
        (fraction_of_charged_residues >= 0.25) & (fraction_of_charged_residues <= 0.35),         # Region 2
        (fraction_of_charged_residues > 0.35) & (ncpr < 0.35),                # Region 3
        (fraction_of_positively_charged_residues > 0.35),                     # Region 4
        (fraction_of_negatively_charged_residues > 0.35)                      # Region 5
    ]

    color_choices = ["rgb(138.0,251.0,69.0)", 
                     "rgb(254.0,230.0,90.0)", 
                     "mediumorchid", 
                     "blue", 
                     "red"]

    blob_properties_df["color_for_daspappu_track"] = np.select(conditions, color_choices, default="Error")

    # This case is impossible but here for completeness
    if (blob_properties_df["color_for_daspappu_track"] == "Error").any():
         raise Exception("Found inaccessible region of Das-Pappu phase diagram.")

    return blob_properties_df

def assign_blob_predicted_dsnp_enrichment_color(blob_properties_df):
    """
    Assigns the color for each blob based on how sensitive to mutation it is predicted to be.
    Note: This function requires the minimum smoothed hydropathy for each blob. The analysis from 
        Lohia et al. 2022 that produced the data by which blobs are colored involved increasing the H* 
        threshold, and the minimum smoothed hydropathy is what determines that any given h-blob of a 
        given length is still considered an h-blob as this threshold is increased.
    
    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the number of residues in the blob, the minimum smoothed hydropathy, and the type of blob it is

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing the color value for each residue based on how sensitive to a mutation the blob that contains the residue is predicted to be
    """

    lookup_keys = list(zip(blob_properties_df["blob_minimum_hydrophobicity"].round(2), blob_properties_df["blob_length"]))

    h_colors = enrich_df["color"].reindex(lookup_keys).fillna("grey").values
    p_colors = enrich_df_p["color"].reindex(lookup_keys).fillna("grey").values
    s_colors = enrich_df_s["color"].reindex(lookup_keys).fillna("grey").values

    conditions = [
        (blob_properties_df["residue_blob_type"] == "h"),
        (blob_properties_df["residue_blob_type"] == "p"),
        (blob_properties_df["residue_blob_type"] == "s")
    ]
    
    choices = [h_colors, p_colors, s_colors]

    blob_properties_df["color_for_dsnp_enrichment_track"] = np.select(conditions, choices, default="grey")

    return blob_properties_df

def assign_blob_uversky_color(blob_properties_df):
    """
    Assigns the color for each blob based on its distance from the disorder/order boundary on the Uversky diagram

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the uversky distances for each residue by blob

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing a column called "color_for_uversky_track" containing the color associated to the distance from the disorder/order boundary on the Uversky diagram for each residue based on the blob that it is contained in
    """
    distances = blob_properties_df["blob_distance_from_uversky_boundary_line"].round(2)

    blob_properties_df["color_for_uversky_track"] = distances.map(uverskyDict).fillna("grey")
    
    return blob_properties_df

def assign_blob_disorder_color(blob_properties_df):
    """
    Assigns the color value for each blob based on how disordered it is which is determined by the Uniprot accession

    Arguments:
        blob_properties_df (pd.DataFrame): A dataframe containing the disorder value for each residue by blob

    Returns:
        blob_properties_df (pd.DataFrame): A dataframe containing a column called "color_for_disorder_predictor_track" containing the color associated to the disorder value for each residue based on the blob that it is contained in.
    """
    blob_disorder = blob_properties_df["blob_disorder"].round(2)

    blob_properties_df["color_for_disorder_predictor_track"] = blob_disorder.map(disorderDict).fillna("grey")

    return blob_properties_df

def assign_colors(blob_properties_df, color_types=None):
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
        blob_properties_df (pandas.DataFrame): The dataframe to assign colors to.
        color_types (list of str, optional): A list of which color tracks to compute. Defaults to all tracks.

    Returns:
        blob_properties_df (pandas.DataFrame): The dataframe with the assigned colors.
    """
    if color_types is None:
        color_types = ["blobtype", "dsnp_enrichment", "daspappu", "NCPR", "uversky", "disorder"]
    if "blobtype" in color_types:
        blob_properties_df = assign_blob_color_by_type(blob_properties_df)
    if "NCPR" in color_types:
        blob_properties_df = assign_blob_ncpr_color(blob_properties_df)
    if "daspappu" in color_types:
        blob_properties_df = assign_blob_das_pappu_color(blob_properties_df)
    if "dsnp_enrichment" in color_types:
        blob_properties_df = assign_blob_predicted_dsnp_enrichment_color(blob_properties_df)
    if "uversky" in color_types:
        blob_properties_df = assign_blob_uversky_color(blob_properties_df)
    if "disorder" in color_types:
        blob_properties_df = assign_blob_disorder_color(blob_properties_df)

    return blob_properties_df

def clean_df(blob_properties_df):
    """
    Removes unnecessary columns from a given dataframe

    Arguments:
        blob_properties_df (dataframe): A pandas dataframe

    Returns:
        blob_properties_df (dataframe): A cleaned pandas dataframe
    """
    del blob_properties_df["residue_blob_type_pre"]
    del blob_properties_df["color_for_NCPR_track"]
    del blob_properties_df["color_for_blobtype_track"]
    del blob_properties_df["color_for_daspappu_track"]
    del blob_properties_df["color_for_uversky_track"]
    del blob_properties_df["color_for_disorder_predictor_track"]
    del blob_properties_df["hydropathy_digitized"]
    del blob_properties_df["residue_charge"]
    # del blob_properties_df["assign_residue_track_bar_height"]
    del blob_properties_df["residue_disorder"]
    blob_properties_df["residue_number"] = blob_properties_df["residue_number"].astype(int)
    
    blob_properties_df = blob_properties_df[[ "residue_number",
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
    
    blob_properties_df = blob_properties_df.rename(columns={"residue_name": "Residue",
                            "residue_number": "Residue_Position", 
                            "blob_disorder": "Blob_Disorder_Score", 
                            "smoothing_window_length": "Window_Length", 
                            "hydropathy_cutoff": "Hydropathy_Cutoff", 
                            "blob_length_minimum": "Minimum_Blob_Length", 
                            "residue_blob_type":"Blob_Type", 
                            "blob_hydrophobicity": "Normalized_Mean_Blob_Hydropathy",
                            "blob_minimum_hydrophobicity": "Minimum_Blob_Hydropathy", 
                            "residue_blob_groups": "Blob_Name", 
                            "blob_net_charge_per_residue": "Blob_NCPR", 
                            "blob_fraction_of_positively_charged_residues": "Fraction_of_Positively_Charged_Residues", 
                            "blob_fraction_of_negatively_charged_residues": "Fraction_of_Negatively_Charged_Residues", 
                            "blob_fraction_of_charged_residues": "Fraction_of_Charged_Residues", 
                            "blob_predicted_enrichment_of_dsnps": "dSNP_Enrichment", 
                            "blob_daspappu_phase": "Blob_Das-Pappu_Class", 
                            "blob_distance_from_uversky_boundary_line": "Uversky_Diagram_Score", 
                            "residue_hydropathy": "Normalized_Hydropathy",
                            "residue_smoothed_hydropathy": "Smoothed_Hydropathy",
                            "blob_length": "Blob_Length"})
    #blob_properties_df["Kyte-Doolittle_hydropathy"] = blob_properties_df["Normalized_Kyte-Doolittle_hydropathy"]*9-4.5

    return blob_properties_df

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
        blob_properties_df (pandas.DataFrame): A dataframe with the above columns.
    """
    if disorder_residues is None:
        disorder_residues = []

    # Build initial dataframe
    blob_properties_df = build_sequence_df(seq, disorder_residues, hydropathy_scale)

    # Smooth and digitize hydropathy
    blob_properties_df = smooth_and_digitize(blob_properties_df, hydropathy_cutoff, smoothing_window_length)

    # Assign blob types
    blob_properties_df = assign_blob_types(blob_properties_df, blob_length_minimum)

    # Compute blob properties
    blob_properties_df = compute_blob_properties(blob_properties_df)

    # Assign colors
    if include_colors:
        blob_properties_df = assign_colors(blob_properties_df, color_types)

    # Add data to columns
    blob_properties_df["smoothing_window_length"] = smoothing_window_length
    blob_properties_df["hydropathy_cutoff"] = hydropathy_cutoff
    blob_properties_df["blob_length_minimum"] = blob_length_minimum
    blob_properties_df["hydropathy_scale"] = hydropathy_scale
    blob_properties_df["disorder_residues"] = [disorder_residues] * len(blob_properties_df)
    return blob_properties_df
