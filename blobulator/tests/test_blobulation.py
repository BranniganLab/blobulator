import pytest
import blobulator
import os

with open("expected_inputs.txt", 'r') as ifile:
    test_data=[]
    for line in ifile:
        line = line.strip()
        line = line.split(", ")
        test_data.append(line)

class TestBlobulation:
    @pytest.mark.parametrize("sequence, cutoff, min_blob, oname", test_data)
    def test_sequence_outputs(self, sequence:str, cutoff:float, min_blob:int, oname:str, hscale='kyte_doolittle'):

        blobDF = blobulator.compute(sequence, float(cutoff), int(min_blob), hscale)
        blobDF = blobulator.clean_df(blobDF)
        blobDF.to_csv(f"test_outputs/{oname[0:-13]}.csv", index=False)

        expected = [row for row in open(oname)]
        test = [row for row in open(f"test_outputs/{oname[0:-13]}.csv")]

        assert expected == test