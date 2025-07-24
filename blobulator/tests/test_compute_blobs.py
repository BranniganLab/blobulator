import pytest
import blobulator
import pandas as pd
from pandas import testing as tm
import os

@pytest.fixture
def current_blobulation():
    sequence = "RRRRRRRRRIIIIIIIII"
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
    assert tm.assert_series_equal(current_blobulation["Min_Blob_Hydropathy"], previous_blobulator_output["Min_Blob_Hydropathy"])

def test_blob_index_number(current_blobulation, previous_blobulator_output):
    """ Tests that the index column is consistent between both the old and new blobulator outputs"""
    assert tm.assert_series_equal(current_blobulation["Blob_Index_Number"], previous_blobulator_output["Blob_Index_Number"])

def test_blob_ncpr(current_blobulation, previous_blobulator_output):
    """ Tests that the NCPR column is consistent between both the old and new blobulator outputs"""
    assert current_blobulation["Blob_NCPR"], previous_blobulator_output["Blob_NCPR"])

def test_blob_dsnp_enrichment(current_blobulation, previous_blobulator_output):
    """ Tests that the dSNP_enrichment column is consistent between both the old and new blobulator outputs"""
    assert tm.assert_series_equal(current_blobulation["dSNP_enrichment"], previous_blobulator_output["dSNP_enrichment"])

def test_blob_daspappu(current_blobulation, previous_blobulator_output):
    """ Tests that the Das-Pappu class column is consistent between both the old and new blobulator outputs"""
    assert tm.assert_series_equal(current_blobulation["Blob_Das-Pappu_Class"], previous_blobulator_output["Blob_Das-Pappu_Class"])

def test_blob_uversky(current_blobulation, previous_blobulator_output):
    """ Tests that the uversky column is consistent between both the old and new blobulator outputs"""
    assert tm.assert_series_equal(current_blobulation["Uversky_Diagram_Score"], previous_blobulator_output["Uversky_Diagram_Score"])

def test_kytedoolittle_hydropathy(current_blobulation, previous_blobulator_output):
    """ Tests that the Kyte-Doolittle hydropathy column is consistent between both the old and new blobulator outputs"""
    assert tm.assert_series_equal(current_blobulation["Kyte-Doolittle_hydropathy"], previous_blobulator_output["Kyte-Doolittle_hydropathy"])

