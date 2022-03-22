# Protein Blobulator
_Looking for the webinterface? Try here:_ https://www.blobulator.branniganlab.org/ 

This tool identifies contiguous stretches of hydrophobic residues within a protein sequence. Any sequence of contiguous hydrophobic residues that is at least as long as the minimum blob length is considered an hydrophobic or h "blob". Any remaining segments that are at least as long as the minimum length are considered polar or p "blobs," while those that are shorter than the minimum blob length are considered separator or "s" residues.  Separator residues are very short stretches of non-hydrophobic residues that may be found between two h blobs.

## Running locally:

### Installation guide:

#### Software requirements:
```
Python 3.9+
```
#### Python dependencies:
```
wtforms
pandas
matplotlib
flask
flask_restful
flask_cors
flask_session
requests
svglib
biopython
argparse
reportlab
flask (website version)
```

#### Quick Install:
Download from github:
```
git clone https://github.com/BranniganLab/blobulator
```
Using conda:
```
conda create --name blobulator_env python=3.9
conda activate blobulator_env
pip install -r requirements.txt
```

### Running through an internet browser:
Note: this option is identical to the website version, but may run faster:
```
python blobulation.py
```

### Running from the command line:
#### Basic usage:
Open a terminal in the blobulator directory and run:
```
python3 compute_blobs.py --sequence AFRPGAGQPPRRKECTPEVEEGV --oname ./my_blobulation.csv
```
This will blobulate the sequence "AFRPGAGQPPRRKECTPEVEEGV" and write the result to my_blobulation.csv

#### Options:
You may specify additional paramters using the following options:
```
-h, --help           show help information and exit

--sequence SEQUENCE  Takes a single string of EITHER DNA or protein one-letter codes (no spaces).
--cutoff CUTOFF      Sets the cutoff hydrophobicity (floating point number between 0.00 and 1.00 inclusive). Defaults to 0.4
--minBlob MINBLOB    Mininmum blob length (integer greater than 1). Defaults to 4
--oname ONAME        Name of output file or path to output directory. Defaults to blobulated_.csv
--fasta FASTA        FASTA file with 1 or more sequences
--DNA DNA            Flag that says whether the inputs are DNA or protein. Defaults to false (protein)
```
#### Advanced Usage (FASTA files):
- Place a fasta file with one or more sequences in any directory (Note: they must all be DNA or protein sequences)
- Open a terminal in the blobulator directory and run:
```
python3 compute_blobs.py --fasta /relative/path/to/my_sequences.fasta --oname ./relative/path/to/outputs/
```
- This will blobulate all sequences in my_sequences.fasta (assuming they are protein sequences) and output the results to the outputs folder prefixed by their sequence id.

#### Example:
There is a fasta file in blobulation/Batch called ls_orchid.fasta that contains the coding sequences of several orchid proteins.
To blobulate all those proteins with a cutoff of 0.4 and a minimum blob size of 4, we run:
```
mkdir ./Batch/Outputs
python3 compute_blobs.py --fasta ./Batch/ls_orchid.fasta --DNA True --cutoff 0.4 --minBlob 4 --oname ./Batch/Outputs/
```

### CSV Outputs:
Whether you have blobulated your proteins of interest using the web utility or the command-line option, you can obtain the blobulation data as a csv (the only output of the command line option or by clicking "Download Data" on the website).
These CSVs are organized with each residue in its own row and columns as follows:
- Residue_Number: The position of the residue in the sequence starting at 1
- Residue_Name: The one-letter amino acid code
- Window: The size of the rolling average window (this is currently 3 by default. We have not yet added the ability to change this.)
- Hydropathy_Cutoff: The normalized cutoff used during blobulation (float between 0 and 1)
- Minimum_Blob_Length: The minimum blob length used during blobulation (integer greater than 0)
- blob_length: The length of the residue's blob
- Normalized_Mean_Blob_Hydropathy: The normalized mean hydropathy of the residue's blob
- Blob_Type: The one-letter blob code (h=hydropathic, p=polar/hydrophilic, s=short hydrophilic)
- Blob_Index_Number: Indices which distinguish blobs. E.g. h1 is the first hydrophobic blob. h1a and h1b refer to two halves of a blob separated by a short hydrophobic blob.
- Blob_Das-Pappu_Class: Blob scored by Das-Pappu globularity. 1=globular, 2=Janus/boundary, 3=Polar, 4=Polycation, 5=Polyanion
- Blob_NCPR: Net-charge-per-residue of the blob
- Fraction_of_Positively_Charged_Residues: FPC = N(Positively charged residues)/N(residues)
- Fraction_of_Negatively_Charged_Residues: FNC = N(Negatively charged residues)/N(residues)
- Fraction_of_Charged_Residues: FCR = FPC+FNC
- Uversky_Diagram_Score: Distance from the Uversky-Gillespie-Fink globular/disordered cutoff. See https://pubmed.ncbi.nlm.nih.gov/11025552/
- dSNP_enrichment: Predicted disease-causing mutation enrichment. dSNP_enrichment: Predicted enrichment of disease-causing SNPs. See Lohia, Hansen, and Brannigan, 2022, PNAS, In Press.
- Blob_Disorder: Mean expected disorder score as provided by D2P2. See https://doi.org/10.1093/nar/gks1226
- Normalized_Kyte-Doolittle_hydropathy: K-D hydropathy normalized to be between 0 and 1. See Kyte-Doolittle_hydropathy.
- Kyte-Doolittle_hydropathy: Traditional K-D hydropathy (on a scale from -4.5 to 4.5). This is a very common hydrophobicity scale dating to 1982: https://doi.org/10.1016%2F0022-2836%2882%2990515-0



