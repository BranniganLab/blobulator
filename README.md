#Protein Blobulator



##Steps for running protein blobulation:

### Using common line:

```
Blobulating default sequence with default blobulation parameters of hydropathy cutoff and minimum blob length
python3 blobulation.py
The blobulation parameters can be changed with “compute” function in blobulation.py
compute(seq=“input_seqeunce”, cutoff=0.4, domain_threshold=4)

Output:
The blobulated sequence “blobulated.csv” is saved in current working directory
```
### Using web interface 

https://www.blobulator.branniganlab.org/

### Running web tool from command line

```
python3 blobulation.py and then go to a web browser and run  http://127.0.0.1:5000
```

### Tool Code description:

**blobulation.py** - This is the backbone script of the tool. 
The script uses flask and wtforms module. 
It first reads the user inputed sequence or uniprot id. 
If the user inputs uniprot id, it further makes following calls
  - https://www.ebi.ac.uk/proteins/api/features - to get the sequence of the protein from uniprot id
  - https://www.ebi.ac.uk/proteins/api/variation - to get the disease causing missense SNPs in the given sequence
  - http://d2p2.pro/ - to get the disorder score for each amino acid in the sequence 

**compute_blobs.py** is called with the sequence and its features (when present) to blobulate the protein.
The output of compute_blobs.py (dataframe of blobulated sequence) is then passed to index.html for plotting with d3. 

The api function for the tool is also written here. For eg you can go to your browser and run "http://127.0.0.1:5000//api/query?my_seq=MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA&domain_threshold=24&cutoff=0.5&my_disorder=2,3" , this will output the blobulated protein as a json file.

**compute_blobs.py** - This script takes the amino acid sequence as input and outputs the blob properties for each residue. It also contains function for plotting the downloadable version of the plot.

**index.html** - This script uses javascript to interact with the html elements and draws and updates the blobulated protein. Each time the user changes the input values (moves the slider) the script makes a call to its own api function written in blobulation.py. The api function calls compute_blobs.py with updated input parameters.

**tabs.html** - HTML layout of the blobulator page including documentation and tabs.
