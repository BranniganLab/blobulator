import pytest
import blobulator
import os
import pandas as pd


def test_CI():
    """ Simple test to make sure CI is working"""
    assert True

def test_blobulator():
    """ A test to make sure that the current compute_blobs.py has the same output as the old compute_blobs.py  """

    A very simple oligopeptide and standard settings
    sequence = "RRRRRRRRRIIIIIIIII"
    cutoff = 0.4
    min_blob = 4
    hscale = "kyte_doolittle"

    # Do the blobulation
    blobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)
    
    # Cleanup the dataframe (make it more human-readable)
    blobDF = blobulator.clean_df(blobDF)
    
    # Save it as a csv for later use
    testDF = pd.read_csv("blobulator/tests/test_blob.csv")

    assert blobDF == testDF
    