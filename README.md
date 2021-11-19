# Protein Blobulator
This tool identifies contiguous stretches of hydrophobic residues within a protein sequence. Any sequence of contiguous hydrophobic residues that is at least as long as the minimum blob length is considered an hydrophobic or h "blob". Any remaining segments that are at least as long as the minimum length are considered polar or p "blobs," while those that are shorter than the minimum blob length are considered separator or "s" residues.  Separator residues are very short stretches of non-hydrophobic residues that may be found between two h blobs.


## Software requirements:

```
Python 3.9+
```
## Python dependencies:

```
numpy
pandas
matplotlib
svglib
reportlab
```

## Installation guide:

Download from github:

```
git clone https://github.com/BranniganLab/blobulator
```

## Steps for running blobulator locally:
install conda
conda create --name blobulator_env python=3.9
conda activate blobulator_env
pip install wtforms
pip install pandas
pip install matplotlib
pip install flask
pip install flask_restful
pip install flask_cors
pip install flask_session
pip install requests
pip install svglib
python blobulation.py


## Demo:

To blobulate default sequence with default blobulation parameters of hydrophobicity threshold and minimum blob length:
```
cd blobulator
python3 compute_blobs.py
```
The protein seqeunce and blobulation parameters can be changed with “compute” function in compute_blobs.py (line #473)
```
compute(seq, hydrophobicity_threshold, minimum_blob_length)
```
Current defaluts for compute function

```
compute("MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATV", 0.4, 4)
```

Output:
```
The blobulated sequence “blobulated.csv” is written in current working directory
```

## Instructions for use:

Run the compute function for any desired user amino acid sequence, hydrophobicity_threshold and minimum_blob_length:

eg. For running blobulation for 'Small muscular protein (UNIPROT: Q9UHP9)' with hydrophobicity_threshold='0.4' and minimum_blob_length='4'

Obtain the amino acid sequence of Small muscular protein: MNMSKQPVSNVRAIQANINIPMGAFRPGAGQPPRRKECTPEVEEGVPPTSDEEKKPIPGAKKLPGPAVNLSEIQNIKSELKYVPKAEQ

Change the input value of compute function in compute_blobs.py at line #473:

```
compute("MNMSKQPVSNVRAIQANINIPMGAFRPGAGQPPRRKECTPEVEEGVPPTSDEEKKPIPGAKKLPGPAVNLSEIQNIKSELKYVPKAEQ", 0.4, 4)
```
Run compute_blobs.py with new inputs

```
cd blobulator
python3 compute_blobs.py
```

## Web Interface

A web interface for this tool is currently under active development. The beta version can be found at https://www.blobulator.branniganlab.org/


