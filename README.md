# Protein Blobulator
_Looking for the web interface? Find it here:_ https://www.blobulator.branniganlab.org/ 

This tool identifies contiguous stretches of hydrophobic residues within a protein sequence. Any sequence of contiguous hydrophobic residues that is at least as long as the minimum blob length is considered an hydrophobic or h "blob". Any remaining segments that are at least as long as the minimum length are considered polar or p "blobs," while those that are shorter than the minimum blob length are considered separator or "s" residues.  Separator residues are very short stretches of non-hydrophobic residues that may be found between two h blobs.

## Running locally:

### Installation guide:

#### Software requirements:
```
Python 3.9+
```


#### Quick Install:
[**Optional**] Create a conda environment:
```
conda create --name blobulator_env python=3.9
conda activate blobulator_env
```
[**For website and sample scripts**] Download the repository:
```
git clone https://github.com/BranniganLab/blobulator
```
**Install with pip**
```
pip install git+https://github.com/BranniganLab/blobulator
```
**Known issue:**
If you get an error installing pycairo, try ```conda install pycairo``` and retry the above.

### Running through an internet browser:
Note: this option is identical to the website version, but is hosted on your local machine:
```
cd [path_to_repository]/website
python3 blobulation.py
```
If a browser doesn't open automatically, copy the url from the terminal into a browser.

### Scripting - Hello, World:

```
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
    oname = "hello_blob.csv"
    blobDF.to_csv(oname, index=False)
```
Additional sample scripts can be found in the repository examples directory.


### Using the command-line utility blobulate.py:
#### Minimal Install:
The backend can be installed independently using with ``` pip install blobulator ```

#### Basic usage:
Open a terminal in the blobulator directory and run:
```
python3 -m blobulator --sequence AFRPGAGQPPRRKECTPEVEEGV --oname ./my_blobulation.csv
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
python3 -m blobulator --fasta ./relative/path/to/my_sequences.fasta --oname ./relative/path/to/outputs/
```
- This will blobulate all sequences in my_sequences.fasta (assuming they are protein sequences) and output the results to the outputs folder prefixed by their sequence id.

#### Example:
There is a fasta file in blobulation/example called b_subtilis.fasta that contains the sequences of several proteins from Bacillus subtilis.
To blobulate all those proteins with a cutoff of 0.4 and a minimum blob size of 4, we run:
```
mkdir outputs
python3 -m blobulator --fasta ../example/b_subtilis.fasta --cutoff 0.4 --minBlob 4 --oname outputs/
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

# Blobulating proteins in VMD

**A plugin to blobulate protein structures in VMD**

This plugin allows users to blobulate and view blobs on a protein structure in Visual Molecular Dynamics (VMD). The functionality of this plugin is to provide users with an interface by which they can tune parameters and alter the representation of blobs on a given protein structure.

**Software requirements:** 

```VMD```

## Installation guide:

To obtain this plugin, download the following files from the VMD_scripts folder into a single directory:
``` 
blobulation.tcl
Blob_GUI.tcl
normalized_hydropathyscales.tcl
```

## Quickstart:
1. Load a protein into VMD.
2. Access the Tk console via the Extensions dropdown menu `Extensions > Tk Console`.
3. In the Tk console, change directory to the directory where you downloaded the above scripts
`cd /path/to/blobulator/scripts`.
4. Source the plugin `source Blob_GUI.tcl`.
5. Click the blobulate button to generate the corresponding graphical representation in VMD.

## Optional Settings:
* Select the residues you wish to blobulate (defaults to "all").
* Select your desired scale (defaults to "Kyte-Doolittle").
* Adjust the 'Length' and 'Hydrophobicity' thresholds to your chosen parameters (if applicable).
* Select how you color your blobs; blob representations apply to every frame in a loaded trajectory. 
    * Blob Color - Colors by blob type: h-blobs are blue, p-blobs are orange, and s-blobs are green.
    * Blob ID - Colors h-blobs by blob ID, p-blobs are orange, s-blobs are green, and h-blobs are a color from green to blue.
* To remove all representations, click the 'Clear representations' button.
* Clicking the 'Default' buttons will return the threshold buttons to their default positions.
    * For 'Length', the default will always be set to 4.
    * For 'Hydrophobicity', this value updates depending on the Hydropathy Scale. 
    * To automatically assign the default value when switching scales, click the 'Auto-Update Threshold' checkbox. 

### How to access blob representations: 

The blobulation algorithm will apply all blob types to the VMD user and user2 values.

The 'user' value will store the type of blob: user 1 -> h-blobs, user 2 -> s-blobs, and user 3 -> p-blobs.

The 'user2' value will store the blob group: user2 1 -> h-blob group 1, user2 2 -> s-blob group 1, user2 3 -> h-blob group 2, etc.

When coloring by Blob ID, h-blobs will have different colors depending on the user2 value.    

### Known Limitations:

VMD blobulator can not run its blobulation algorithm on proteins that contain non-standard amino acids.
