import blobulator

# A very simple oligopeptide and standard settings
sequence = "RRRRRRRRRIIIIIIIII"
cutoff = 0.4
min_blob = 4
hscale = "kyte_doolittle"

# Do the blobulation
blobDF = blobulator.compute(sequence, cutoff, min_blob, hscale)

# Cleanup the dataframe (make it more human-readable)
blobDF = blobulator.clean_df(blobDF)

# Save it as a csv for later use
oname = "test_blob.csv"
blobDF.to_csv(oname, index=False)