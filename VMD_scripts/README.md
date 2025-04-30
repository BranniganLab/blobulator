# VMD Blobulation

**A VMD application for blobulation needs**

This tool is a visualization tool for Blobulator using VMD. Blobulator tracks each amino 
acid in a sequence of a human protein to determine consecutive hydrophobic stretches.  If a stretch in the 
amino acid chain is hydrophobic, and longer than the
threshold, it is considered a h blob. If a stretch in the amino acid chain is non-hydrophobic, and longer than the 
threshold, it is considered a p blob. All other stretches are too short and
are categorized as s blobs.  

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

### Using in VMD:

Keep all files in one directory, in the VMD program access the Tk console
from the Extensions drop down menu 
`Extensions > Tk Console`

Using the Linux cd command, cd to the downloaded file location.
Below is an example of accessing the Blob_GUI.tcl file in the Tk console. 

``` cd /path/to/file/Blob_GUI.tcl ``` 

You will need to source everytime you wish to load the Plugin.

### How to access blobulation values: 

The blobulation algorithm will apply all blobs types to the VMD user and user2 values.

User will store the type of blob it is, user 1 -> h-blobs, user 2 -> s-blobs, user 3 -> p-blobs.

User2 will store the blob group, user2 1 -> h-blob group 1, user2 2 -> s-blob group 1, user2 3 -> h-blob group 2, etc.

When coloring by Blob ID, h-blobs will have different colors depending on the user2 value.    

### Known Limitations:

VMD blobulator can not run its blobulation algorithm on proteins that contain
non-standard amino acids
