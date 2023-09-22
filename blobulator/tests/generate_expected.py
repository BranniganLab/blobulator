"""
A Hello-World for blobulation in a python script. Blobulate 
"""

import blobulator
import random
import numpy as np

ntests=20
amino_acids=['A', 'R', 'N', 'D', 'B', 'C', 'E', 'Q', 'Z', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
cutoffs = np.linspace(0,1,ntests)

for num in range(20):
    # A very simple oligopeptide
    sequence = ''.join(random.choices(amino_acids, k=100))

    # Default cutoff, Lmin, and hydrophobicity scale
    cutoff = cutoffs[num]
    min_blob = random.randint(1,30)
    hscale = "kyte_doolittle"

    # Output name
    oname = f"{num}_expected.csv"

    #print(f'Running...\nseq: {sequence}\ncutoff: {cutoff}\nminBlob: {min_blob}\nOutput to: {oname}')
    print(f'{sequence}, {cutoff}, {min_blob}, {oname}')
    blobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)
    #print ("Writing output file")
    blobDF = blobulator.clean_df(blobDF)
    blobDF.to_csv(oname, index=False)
