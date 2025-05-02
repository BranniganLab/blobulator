# VMD Blobulation

**A VMD application for blobulation needs**

This tool is a visualization tool for Blobulator using VMD. The blobulator tracks each amino 
acid in a human protein sequence to determine consecutive hydrophobic stretches. If a stretch in the 
amino acid chain is hydrophobic and longer than the
threshold, it is considered a h-blob. If a stretch in the amino acid chain is non-hydrophobic and longer than the 
threshold, it is a p-blob. All other stretches are too short and
categorized as s-blobs. 

## How to use VMD Blobulation:

### Installation guide:

**Software requirements:** 

```VMD```

**Files Needed:**

``` 
blobulation.tcl
Blob_GUI.tcl
normalized_hydropathyscales.tcl
```
Users can download these in the VMD_scripts folder.

### Using blobulation in VMD:

Keep all files in one directory; in the VMD program, access the Tk console
from the Extensions drop-down menu 
`Extensions > Tk Console`

Using the Linux cd command, cd to the downloaded file location.
Below is an example of accessing the Blob_GUI.tcl file in the Tk console. 

``` cd /path/to/blobulator/VMD_scripts ``` 
```source Blob_GUI.tcl```

You must source Blob_GUI.tcl every time you wish to load the Plugin.

### VMD Plugin Features

The VMD plugin offers a quick and easy method to apply the blobulation algorithm to most
human proteins. 
1. Select the MolID you wish to blobulation (defaults to "top")
2. Select the residues you wish to blobulate (defaults to "all") 
3. Select your desired scale (defaults to "Kyte-Doolittle") 
4. Adjust the 'Length' and 'Hydrophobicity' thresholds to your liking
5. Select how you color your blobs; blob representations apply to every frame in a simulation. 
    a. Blob Color - Colors by blob type: h-blobs are blue, p-blobs are orange, and s-blobs are green
    b. Blob ID - Colors h-blobs by blob ID, p-blobs are orange, s-blobs are green, and h-blobs are a color from green to blue.
6. Click the blobulate button to generate the graphical representation in VMD. 
7. To remove all representations, click the 'Clear representation' button

The 'Default' buttons will return the threshold buttons to their default positions. 
For 'Length', this will always be set to 4. For 'Hydrophobicity', this value changes depending
on the Hydropathy Scale. To automatically assign the default value when switching scales, click the 'Auto Updates Hydrophobicity' checkbox. 

### How to access blobulation values: 

The blobulation algorithm will apply all blob types to the VMD user and user2 values.

The 'user' value will store the type of blob: user 1 -> h-blobs, user 2 -> s-blobs, and user 3 -> p-blobs.

The 'user2' value will store the blob group: user2 1 -> h-blob group 1, user2 2 -> s-blob group 1, user2 3 -> h-blob group 2, etc.

When coloring by Blob ID, h-blobs will have different colors depending on the user2 value.    

### Known Limitations:

VMD blobulator can not run its blobulation algorithm on proteins that contain
non-standard amino acids.
