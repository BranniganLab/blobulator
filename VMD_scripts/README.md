# VMD Regression Testing
The VMD blobulator needs to periodically be compared to the python blobulator code to ensure both algorithms behave the same.
This repo contains two files needed to run this regression test.
```
blobCheck.tcl
compare_to_blobulator.py
```

## Steps to use regression scripts
1. The script pipeline start by taking a pdb file in VMD, generating the blob assignments and storing those assignments in a file named blobTest.csv.
2. Once generated acquire the FATSA sequence of the pbd file on the pdb website: https://www.rcsb.org/.
3. Copy the FATSA sequence into compare_to_blobulator.py, a comment will mark the line to insert the sequence. 
4. Run compare_to_blobulator.py and it'll confirm any mismatched and at what index the mismatch occured. 

### Example sequence
compare_to_blobulator.py by default contains the FATSA sequence for alpha synuclien:https://www.rcsb.org/structure/1XQ8
