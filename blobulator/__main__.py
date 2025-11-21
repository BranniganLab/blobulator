"""
A command-line utility for blobulating. Especially useful for fasta files. 
Demonstrates most blobulator functionality.

Arguments:
  -h, --help           show this help message and exit
  --sequence SEQUENCE  Takes a single string of EITHER DNA or protein one-letter codes (no spaces).
  --cutoff CUTOFF      Sets the cutoff hydrophobicity (floating point number between 0.00 and 1.00 inclusive).
                       Defaults to 0.4
  --minBlob MINBLOB    Mininmum blob length (integer greater than 1). Defaults to 4
  --oname ONAME        Name of output file or path to output directory. Defaults to blobulated_.csv
  --fasta FASTA        FASTA file with 1 or more sequences
  --DNA DNA            Flag that says whether the inputs are DNA or protein. Defaults to false (protein)
"""

if __name__ == "__main__":

    #For diagnostics/development benchmarking
    #import cProfile

    #seq = "MAQILPIRFQEHLQLQNLGINPANIGFSTLTMESDKFICIREKVGEQAQVVIIDMNDPSNPIRRPISADSAIMNPASKVIALKAGKTLQIFNIEMKSKMKAHTMTDDVTFWKWISLNTVALVTDNAVYHWSMEGESQPVKMFDRHSSLAGCQIINYRTDAKQKWLLLTGISAQQNRVVGAMQLYSVDRKVSQPIEGHAASFAQFKMEGNAEESTLFCFAVRGQAGGKLHIIEVGTPPTGNQPFPKKAVDVFFPPEAQNDFPVAMQISEKHDVVFLITKYGYIHLYDLETGTCIYMNRISGETIFVTAPHEATAGIIGVNRKGQVLSVCVEEENIIPYITNVLQNPDLALRMAVRNNLAGAEELFARKFNALFAQGNYSEAAKVAANAPKGILRTPDTIRRFQSVPAQPGQTSPLLQYFGILLDQGQLNKYESLELCRPVLQQGRKQLLEKWLKEDKLECSEELGDLVKSVDPTLALSVYLRANVPNKVIQCFAETGQVQKIVLYAKKVGYTPDWIFLLRNVMRISPDQGQQFAQMLVQDEEPLADITQIVDVFMEYNLIQQCTAFLLDALKNNRPSEGPLQTRLLEMNLMHAPQVADAILGNQMFTHYDRAHIAQLCEKAGLLQRALEHFTDLYDIKRAVVHTHLLNPEWLVNYFGSLSVEDSLECLRAMLSANIRQNLQICVQVASKYHEQLSTQSLIELFESFKSFEGLFYFLGSIVNFSQDPDVHFKYIQAACKTGQIKEVERICRESNCYDPERVKNFLKEAKLTDQLPLIIVCDRFDFVHDLVLYLYRNNLQKYIEIYVQKVNPSRLPVVIGGLLDVDCSEDVIKNLILVVRGQFSTDELVAEVEKRNRLKLLLPWLEARIHEGCEEPATHNALAKIYIDSNNNPERFLRENPYYDSRVVGKYCEKRDPHLACVAYERGQCDLELINVCNENSLFKSLSRYLVRRKDPELWGSVLLESNPYRRPLIDQVVQTALSETQDPEEVSVTVKAFMTADLPNELIELLEKIVLDNSVFSEHRNLQNLLILTAIKADRTRVMEYINRLDNYDAPDIANIAISNELFEEAFAIFRKFDVNTSAVQVLIEHIGNLDRAYEFAERCNEPAVWSQLAKAQLQKGMVKEAIDSYIKADDPSSYMEVVQAANTSGNWEELVKYLQMARKKARESYVETELIFALAKTNRLAELEEFINGPNNAHIQQVGDRCYDEKMYDAAKLLYNNVSNFGRLASTLVHLGEYQAAVDGARKANSTRTWKEVCFACVDGKEFRLAQMCGLHIVVHADELEELINYYQDRGYFEELITMLEAALGLERAHMGMFTELAILYSKFKPQKMREHLELFWSRVNIPKVLRAAEQAHLWAELVFLYDKYEEYDNAIITMMNHPTDAWKEGQFKDIITKVANVELYYRAIQFYLEFKPLLLNDLLMVLSPRLDHTRAVNYFSKVKQLPLVKPYLRSVQNHNNKSVNESLNNLFITEEDYQALRTSIDAYDNFDNISLAQRLEKHELIEFRRIAAYLFKGNNRWKQSVELCKKDSLYKDAMQYASESKDTELAEELLQWFLQEEKRECFGACLFTCYDLLRPDVVLETAWRHNIMDFAMPYFIQVMKEYLTKVDKLDASESLRKEEEQATETQPIVYGQPQLMLTAGPSVAVPPQAPFGYGYTAPPYGQPQPGFGYSM"
    #cProfile.run("compute(seq, 0.4, 4)")
    #for i in range(1,len(seq), 5):
     #   cProfile.run("compute(seq[0:i], 0.4, 4)")

    #df = compute("MSPQTETKASVGFKAGVKDYKLTYYTPEYETKDTDILAAFRVTPQPGVPPEEAGAAVAAESSTGTWTTVWTDGLTSLDRYKGRCYHIEPVAGEENQYICYVAYPLDLFEEGSVTNMFTSIVGNVFGFKALRALRLEDLRIPTAYVKTFQGPPHGIQVERDKLNKYGRPLLGCTIKPKLGLSAKNYGRAVYECLRGGLDFTKDDENVNSQPFMRWRDRFLFCAEAIYKSQAETGEIKGHYLNATAGTCEEMMKRAIFARELGVPIVMHDYLTGGFTANTSLAHYCRDNGLLLHIHRAMHAVIDRQKNHGIHFRVLAKALRMSGGDHIHSGTVVGKLEGERDITLGFVDLLRDDFIEKDRSRGIYFTQDWVSLPGVLPVASGGIHVWHMPALTEIFGDDSVLQFGGGTLGHPWGNAPGAVANRVALEACVQARNEGRDLAREGNEIIREACKWSPELAAACEVWKEIKFEFQAMDTL", 0.4, 1)
    
    import argparse
    from Bio import SeqIO
    from Bio.Seq import Seq
    import blobulator
    import time
    start = time.time()

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--sequence', type=str, help='Takes a single string of EITHER DNA or protein one-letter codes (no spaces).', default=None)
    parser.add_argument('--cutoff', type=float, help='Sets the cutoff hydrophobicity (floating point number between 0.00 and 1.00 inclusive). Defaults to 0.4', default=0.4)
    parser.add_argument('--minBlob', type=int, help='Mininmum blob length (integer greater than 1). Defaults to 4', default=4)
    parser.add_argument('--oname', type=str, help='Name of output file or path to output directory. Defaults to blobulated_.csv', default="blobulated_")
    parser.add_argument('--fasta', type=str, help='FASTA file with 1 or more sequences', default=None)
    parser.add_argument('--DNA', type=bool, help='Flag that says whether the inputs are DNA or protein. Defaults to false (protein)', default=False)
    
    # New argument to allow selection of specific computations
    parser.add_argument('--compute', type=str, nargs='+', default=['all'],
                        choices=["all", "length", "hydrophobicity", "min_hydro", "ncpr",
                                 "disorder", "charges", "order", "pred_enrichment"],
                        help="Specify which blob properties to compute. Use 'all' to run everything.")

    args = parser.parse_args()

    if args.DNA:
        print("REMINDER: The blobulator assumes all DNA inputs to be coding sequences and only translates up to the first stop codon.")
        print("CAUTION: Do not mix DNA and protein sequences")
    if (args.sequence is not None) & (args.fasta is not None):
        print("ERROR: Input EITHER --sequence OR --fasta. NOT both.")

    elif args.fasta:
        print(f"Reading {args.fasta}")
        for seq_record in SeqIO.parse(args.fasta, "fasta"):
            print(f'Running: {seq_record.id}')
            if args.DNA:
                coding_dna = seq_record.seq
                mrna = coding_dna.transcribe()
                sequence = mrna.translate(to_stop=True)
            else:
                sequence = seq_record.seq

            if "all" in args.compute:
                df = blobulator.compute(sequence, args.cutoff, args.minBlob, 'kyte_doolittle')
            else:
                df = blobulator.build_sequence_df(sequence)
                df = blobulator.smooth_and_digitize(df, args.cutoff)
                df = blobulator.assign_blob_types(df, args.minBlob)

                if "length" in args.compute: df = blobulator.compute_blob_length(df)
                if "hydrophobicity" in args.compute: df = blobulator.compute_blob_hydrophobicity(df)
                if "min_hydro" in args.compute: df = blobulator.compute_blob_min_hydrophobicity(df)
                if "ncpr" in args.compute: df = blobulator.compute_blob_ncpr(df)
                if "disorder" in args.compute: df = blobulator.compute_blob_disorder(df)
                if "charges" in args.compute: df = blobulator.compute_blob_charge_property(df)
                if "order" in args.compute: df = blobulator.compute_blob_order(df)
                if "pred_enrichment" in args.compute: df = blobulator.compute_blob_predicted_enrichment(df)

            df = blobulator.clean_df(df)
            print(f"Writing output file to: {args.oname}{seq_record.id}.csv")
            df.to_csv(f'{args.oname}{seq_record.id}.csv', index=False)

    elif args.sequence:
        print(f'Running...\nseq: {args.sequence}\ncutoff: {args.cutoff}\nminBlob: {args.minBlob}\nOutput to: {args.oname}')
        if args.DNA:
            coding_dna = Seq(args.sequence)
            mrna = coding_dna.transcribe()
            sequence = mrna.translate(to_stop=True)
        else:
            sequence = args.sequence

        if "all" in args.compute:
            df = blobulator.compute(sequence, args.cutoff, args.minBlob, 'kyte_doolittle')
        else:
            df = blobulator.build_sequence_df(sequence)
            df = blobulator.smooth_and_digitize(df, args.cutoff)
            df = blobulator.assign_blob_types(df, args.minBlob)

            # Run only requested computations
            if "length" in args.compute: df = blobulator.compute_blob_length(df)
            if "hydrophobicity" in args.compute: df = blobulator.compute_blob_hydrophobicity(df)
            if "min_hydro" in args.compute: df = blobulator.compute_blob_min_hydrophobicity(df)
            if "ncpr" in args.compute: df = blobulator.compute_blob_ncpr(df)
            if "disorder" in args.compute: df = blobulator.compute_blob_disorder(df)
            if "charges" in args.compute: df = blobulator.compute_blob_charge_property(df)
            if "order" in args.compute: df = blobulator.compute_blob_order(df)
            if "pred_enrichment" in args.compute: df = blobulator.compute_blob_predicted_enrichment(df)

        df = blobulator.clean_df(df)
        print ("Writing output file")
        df.to_csv(args.oname, index=False)

        print("done")
    else:
        print("No sequence provided")
    end = time.time()
    print(f"compute_blob_order took {end - start:.4f} seconds")