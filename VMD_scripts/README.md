## Installation

Installation instructions for the VMD plugin can be found here: https://github.com/BranniganLab/blobulator/tree/main

### VMD Plugin Features

The VMD plugin offers a quick and easy method to apply the blobulation algorithm to most human proteins. 
1. Select the MolID you wish to blobulate (defaults to "top")
2. Select the residues you wish to blobulate (defaults to "all") 
3. Select your desired scale (defaults to "Kyte-Doolittle") 
4. Adjust the 'Length' and 'Hydrophobicity' thresholds to your chosen parameters
5. Select how you color your blobs; blob representations apply to every frame in a loaded trajectory. 
    a. Blob Color - Colors by blob type: h-blobs are blue, p-blobs are orange, and s-blobs are green
    b. Blob ID - Colors h-blobs by blob ID, p-blobs are orange, s-blobs are green, and h-blobs are a color from green to blue.
6. Click the blobulate button to generate the graphical representation in VMD. 
7. To remove all representations, click the 'Clear representation' button

Clicking the 'Default' buttons will return the threshold buttons to their default positions.
For 'Length', the default will always be set to 4. For 'Hydrophobicity', this value updates depending
on the Hydropathy Scale. To automatically assign the default value when switching scales, click the 'Auto Update Hydrophobicity' checkbox. 

### How to access blobs: 

The blobulation algorithm will apply all blob types to the VMD user and user2 values.

The 'user' value will store the type of blob: user 1 -> h-blobs, user 2 -> s-blobs, and user 3 -> p-blobs.

The 'user2' value will store the blob group: user2 1 -> h-blob group 1, user2 2 -> s-blob group 1, user2 3 -> h-blob group 2, etc.

When coloring by Blob ID, h-blobs will have different colors depending on the user2 value.    

### Known Limitations:

VMD blobulator can not run its blobulation algorithm on proteins that contain non-standard amino acids.
