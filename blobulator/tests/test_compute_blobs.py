import pytest
import blobulator
import pandas as pd

@pytest.fixture
def current_blobulation():
    sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
    cutoff = 0.4
    min_blob = 4
    hscale = "kyte_doolittle"
    
    blobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)
    
    current_blobulation = blobulator.clean_df(blobDF)
    
    return current_blobulation
@pytest.fixture
def previous_blobulator_output():
    previous_blobulator_output = pd.read_csv("blobulator/tests/test_blob.csv")
    return previous_blobulator_output

def test_CI():
    """ Simple test to make sure CI is working"""
    assert True

def test_min_blob_hydropathy(current_blobulation, previous_blobulator_output):
    """ Tests that the hydropathy column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Minimum_Blob_Hydropathy"].round(3).astype(str).equals(previous_blobulator_output["Min_Blob_Hydropathy"].round(3).astype(str))

def test_blob_index_number(current_blobulation, previous_blobulator_output):
    """ Tests that the index column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Blob_Name"].astype(str).equals(previous_blobulator_output["Blob_Index_Number"].astype(str))

def test_blob_ncpr(current_blobulation, previous_blobulator_output):
    """ Tests that the NCPR column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Blob_NCPR"].round(3).astype(str).equals(previous_blobulator_output["Blob_NCPR"].round(3).astype(str))

def test_blob_dsnp_enrichment(current_blobulation, previous_blobulator_output):
    """ Tests that the predicted dSNP enrichment column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["dSNP_Enrichment"].round(3).astype(str).equals(previous_blobulator_output["dSNP_enrichment"].round(3).astype(str))

def test_blob_daspappu(current_blobulation, previous_blobulator_output):
    """ Tests that the Das-Pappu class column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Blob_Das-Pappu_Class"].astype(str).equals(previous_blobulator_output["Blob_Das-Pappu_Class"].astype(str))

def test_blob_uversky(current_blobulation, previous_blobulator_output):
    """ Tests that the Uversky column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Uversky_Diagram_Score"].round(3).astype(str).equals(previous_blobulator_output["Uversky_Diagram_Score"].round(3).astype(str))

from pandas.testing import assert_frame_equal

def test_complete_blobulation_output(current_blobulation, previous_blobulator_output):
    expected = previous_blobulator_output.rename(columns={
        "Residue_Number": "Residue_Position",
        "Residue_Name": "Residue",
        "Window": "Window_Length",
        "blob_length": "Blob_Length",
        "Min_Blob_Hydropathy": "Minimum_Blob_Hydropathy",
        "Blob_Index_Number": "Blob_Name",
        "dSNP_enrichment": "dSNP_Enrichment",
        "Blob_Disorder": "Blob_Disorder_Score",
        "Normalized_hydropathy": "Normalized_Hydropathy",
    })
    expected["Blob_Das-Pappu_Class"] = expected["Blob_Das-Pappu_Class"].astype(str)

    assert_frame_equal(
        current_blobulation.reset_index(drop=True),
        expected.reset_index(drop=True),
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9,
    )
