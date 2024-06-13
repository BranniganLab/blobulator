# VMD Blobulation

**A VMD application for blobulation needs**

This tool is a visualization tool for Blobulator. Blobulator tracks amino 
acid sequences of proteins to determine hydrophobicity. If a section of an 
amino acid chain is hydrophobic, and longer than the
threshold, it is considered a h blob. If a section of
an amino acid chain is hydrophilic, and longer than the 
threshold, it is considered a p blob. All other sections are too short and
are categorized as s blobs.  

## How to use VMD Blobulation: 

### Installation guide:

**Software requirements:** 

```VMD```

**Files Needed:**

``` 
Blobulation.tcl
Blobs_GUI.tcl
normalized_hydropathyscales.tcl
```

### Using in VMD:

Keep all files in one directory, in the VMD program access the Tk console
from the Extensions drop down menu 
`Extensions > Tk Console`

Using the Linux cd command, cd to the downloaded file location.
Below is an example of accessing the proper direcotry in the Tk Console 

``` cd /VMD/blobulator ```
 
 then input the following command 

``` source Blobs_GUI.tcl ``` 

You will need to source everytime you wish to load the GUI. 
