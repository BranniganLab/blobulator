# Protein Blobulator
For any given protein sequece, this tool identifies contigous stretchs of hydrophobic segments. Each residue is assigned to h blobs (hydophobic), p blob (polar) or s (seperator) residues.

## Software requirements:

```
Python 3+
```
## Python dependencies:

```
numpy
pandas
matplotlib
```

## Installation guide:

Download from github:

```
git clone https://github.com/BranniganLab/blobulator
```
## Demo:

Blobulating default sequence with default blobulation parameters of hydrophobicity threshold and minimum blob length:
```
cd blobulator
python3 compute_blobs.py
```
The protein seqeunce and blobulation parameters can be changed with “compute” function in compute_blobs.py:
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
### Using web interface 

https://www.blobulator.branniganlab.org/ (Beta version)

## Instructions for use:

Run the compute function for any desired user amino acid sequence, hydrophobicity_threshold and minimum_blob_length:

eg. For running blobulation for 'Small muscular protein (UNIPROT: Q9UHP9)' with hydrophobicity_threshold='0.4' and minimum_blob_length='4'

Obtain the amino acid sequence of Small muscular protein: MNMSKQPVSNVRAIQANINIPMGAFRPGAGQPPRRKECTPEVEEGVPPTSDEEKKPIPGAKKLPGPAVNLSEIQNIKSELKYVPKAEQ

Change the input value of compute function in compute_blobs.py:

```
compute("MNMSKQPVSNVRAIQANINIPMGAFRPGAGQPPRRKECTPEVEEGVPPTSDEEKKPIPGAKKLPGPAVNLSEIQNIKSELKYVPKAEQ", 0.4, 4)
```
Run compute_blobs.py with new inputs

```
cd blobulator
python3 compute_blobs.py
```



