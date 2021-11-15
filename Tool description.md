### Running web tool from command line

```
python3 blobulation.py and then go to a web browser and run  http://127.0.0.1:5000
```

### Tool API

Go to your browser and run "http://127.0.0.1:5000//api/query?my_seq=MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA&domain_threshold=24&cutoff=0.5&my_disorder=2,3" , this will output the blobulated protein as a json file.

### Tool Code description:

**blobulation.py** - This is the backbone script of the tool. 
The script uses the flask and wtforms modules. 
It first reads the user inputed sequence or uniprot id. 
If the user inputs uniprot id, it further makes following calls
  - https://www.ebi.ac.uk/proteins/api/features - to get the sequence of the protein from a uniprot id
  - https://www.ebi.ac.uk/proteins/api/variation - to get the disease causing missense SNPs in the given sequence
  - http://d2p2.pro/ - to get the disorder score for each amino acid in the sequence 

**compute_blobs.py** is called from blobulation.py with the sequence and its features (when present) to blobulate the protein. This script takes the amino acid sequence as input and outputs the blob properties for each residue. It also contains function for plotting the downloadable version of the plot.
The output of compute_blobs.py (dataframe of blobulated sequence) is then passed to index.html for plotting with d3. 

**index.html**, **result.html**, **figure.js**, etc. - Website providing a user interface for blobulation of proteins. The user may specify a UniProt ID or a protein sequence. Updates in real time as user changes parameters, fetching results from the web API implemented in blobulation.py, which uses compute_blobs.py under the hood.
