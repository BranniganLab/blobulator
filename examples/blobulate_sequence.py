"""
A Hello-World for blobulation in a python script. Blobulate 
"""

import blobulator

# A very simple oligopeptide
sequence = "RRRRRRRRRIIIIIIIII"

# Default cutoff, Lmin, and hydrophobicity scale
cutoff = 0.4
min_blob = 4
hscale = "kyte_doolittle"

# Output name
oname = "hello_blob.csv"

print(f'Running...\nseq: {sequence}\ncutoff: {cutoff}\nminBlob: {min_blob}\nOutput to: {oname}')
blobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)
print ("Writing output file")
blobDF = blobulator.clean_df(blobDF)
blobDF.to_csv(oname, index=False)
