# Changes
## Version 0.8.0
- Added plot colored by blob type
- Updated Uversky plot tooltip
- Misc text edits
- Edited Download Data csv format for clarity
- Fixed "ghost" SNP bug
- Reordered tabs

## Version 0.9.0
- Added zooming function
- Added reset zoom button
- Added tooltips for zoom
- SNPs populate mutation when clicked
- SNPs highlight when hovered over and clicked
- compute_blobs.py accepts FASTA files
- ENSEMBL functionality added
- Additional comments added to backend scripts

## Version 0.9.1
- dSNP enrichment track bug fix
- Clear mutation button added

## Version 0.9.2
- Hydropathy smoothing step bug fix

## Version 0.9.3
- Hydropathy scale now shows where amino acids fall on the given scale
- These letters can be clicked to update the cutoff
- Eisenberg and Weiss hydropathy scale added
- Species, genomic location added to result page
- Uniprot ID is now hyperlinked
- Custom mutations are indicated by diamond shapes
- Custom SNP diamonds clickable
- SNP mutations from uniprot now include rs numbers with clickable links
- X-axis labels prevented from overlapping when zoomed

## Version 0.9.4
- NCPR track bug fix

## Version 0.9.5
- blobulator is now a pip installable package!
- NCPR track rescaled to be between -0.5 and 0.5
- VMD bctool is refactored
- Mutation sensitivity track bug fix
- Group numbering bug fix

## Version 0.9.6
- New heading
- Updated text on About, Documentation, and FAQ pages

## Version 0.9.7
- Added button to lock the control panel to the top of the screen
- Overhauled the home page
- compute_blobs.py variable and function names were updated
- Bug fixes
- Added algorithm description to the 'About' tab
- NCPR track now scaled to be between -0.2 and +0.2

## Version 0.9.8
- Added option to lock conrol panel to the top of the screen on the output page
- rs number popup window stays for longer when mouse hovers over it 
- Minor interface-related bug fixes
- Warning message appears for enrichment of dSNPs in blobs with similar properties track when hydropathy scale is changed from Kyte-Doolittle
- Warning message appears if the aspect ratio of the window matches a cellphone
