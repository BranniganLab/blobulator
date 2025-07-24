import pytest
import blobulator
import pandas as pd
import os

@pytest.fixture
def current_blobulation():
    sequence = "RRRRRRRRRIIIIIIIII"
    cutoff = 0.4
    min_blob = 4
    hscale = "kyte_doolittle"
    
    bltestBlobDFobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)
    
    testBlobDF = blobulator.clean_df(blobDF)
    
    return testBlobDF
@pytest.fixture
def previous_blobulator_output():
    previousBlobDF = pd.read_csv("blobulator/tests/test_blob.csv")
    return previousBlobDF


def test_CI():
    """ Simple test to make sure CI is working"""
    assert True

def test_min_blob_hydropathy(testBlobDF, previousBlobDF):
    """ Tests that the hydropathy column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Min_Blob_Hydropathy"] == previousBlobDF["Min_Blob_Hydropathy"]

def test_blob_index_number(testBlobDF, previousBlobDF):
    """ Tests that the index column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Blob_Index_Number"] == previousBlobDF["Blob_Index_Number"]

def test_blob_ncpr(testBlobDF, previousBlobDF):
    """ Tests that the NCPR column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Blob_NCPR"] == previousBlobDF["Blob_NCPR"]

def test_blob_dsnp_enrichment(testBlobDF, previousBlobDF):
    """ Tests that the dSNP_enrichment column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["dSNP_enrichment"] == previousBlobDF["dSNP_enrichment"]

def test_blob_daspappu(testBlobDF, previousBlobDF):
    """ Tests that the Das-Pappu class column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Blob_Das-Pappu_Class"] == previousBlobDF["Blob_Das-Pappu_Class"]

def test_blob_uversky(testBlobDF, previousBlobDF):
    """ Tests that the uversky column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Uversky_Diagram_Score"] == previousBlobDF["Uversky_Diagram_Score"]

def test_smoothed_hydropathy(testBlobDF, previousBlobDF):
    """ Tests that the smoothed hydropathy column is consistent between both the old and new blobulator outputs"""
    assert testBlobDF["Smoothed_Hydropathy"] == previousBlobDF["Smoothed_Hydropathy"]

