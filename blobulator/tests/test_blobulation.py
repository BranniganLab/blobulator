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
        """
        Perform regression testing by comparing new outputs with canonical outputs.

        Args:
            self: The instance of the TestBlobulation class.
            sequence (str): The DNA sequence to be processed.
            cutoff (float): The cutoff value for blobulation.
            min_blob (int): The minimum blob size.
            oname (str): The name of the output file.
            hscale (str, optional): The hscale parameter for blobulation. Defaults to 'kyte_doolittle'.

        Returns:
            None. The method performs operations on the input parameters and asserts the equality of the generated CSV file with the expected output file.
        """

        blobDF = blobulator.compute(sequence, float(cutoff), int(min_blob), hscale)
        blobDF = blobulator.clean_df(blobDF)
        blobDF.to_csv(f"test_outputs/{oname[0:-13]}_test.csv", index=False, encoding='utf-8')

        expected = list(open(f"canonical_outputs/{oname}", encoding='utf-8'))
        test = list(open(f"test_outputs/{oname[0:-13]}_test.csv", encoding='utf-8'))

        for i, j in zip(expected, test):
            assert i == j