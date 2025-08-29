import blobulator as blob
import pandas as pd
class Blobulator:
    """Representation of blobulated data

       Hidden Attributes:
            __blob (pd.DataFrame): rows with residue information
            __sequence (str): amino acid sequence
            __hydrophobicity_threshold (float): threshold
            __length_threshold (int): threshold 
    """

    def __init__(self, sequence, hydrophobicity_threshold, \
                 length_threshold, hydro_scale="Kyte-Doolittle"):
        self.__blob = (blob.compute(
            sequence, hydrophobicity_threshold, length_threshold))
        self.__sequence = sequence
        self.__hydrophobicity_threshold = hydrophobicity_threshold
        self.__length_threshold = length_threshold
        self.__hydro_scale = hydro_scale

    @property
    def sequence(self):
        return self.__sequence

    def get_domain(self):
        """
        Takes a blobulator data frame, and pulls out the blob domains.
        """

        domain_list = []
        for i in self.__blob["blobtype"]:
            domain_list.append(i)
        return domain_list

    def get_ranges(self):
        """
        Takes a blobulator data frame, and pulls out the blob ranges.
        """
        index = 0
        start_index = 0
        end_index = 0
        is_first = 0
        range_list = []
        character = ''

        if len(set(self.__blob['blobtype'])) == 1:
            residue_ranges = [("N/A", 'N/A')]
            return residue_ranges

        for i in self.__blob['blobtype']:
        
            if i not in character and is_first == 0:
                character = i
                is_first = 1
                start_index = index

                index += 1

            if i not in character and is_first == 1:
                
                character = i
                end_index = index - 2
                range_list.append((start_index, end_index))

                start_index = index - 1

            index += 1

        range_list.append((range_list[-1][-1] + 1, len(self.__sequence) - 1))

        return range_list

    def __len__(self):
        """
        Takes the sequence used for the Blobulator class and finds the length
        """
        return len(self.__sequence)

def read_csv (file):
    df = pd.read_csv(file)
    numbers = df.iloc[:,1].tolist()
    print (len(numbers))
    return numbers

def convert_to_blob_type(num_list):
    blob_list = []
    for number in num_list:
        if number == 1:
            blob_list.append('h')
        if number == 2:
            blob_list.append('s')
        if number ==3:
            blob_list.append('p')
    return blob_list

def compare_lists (list1, list2):
    count = 0
    for entry1, entry2 in zip(list1 , list2):
        if entry1 != entry2:
            print ("mismatch at"+str(count) + entry1+ "/" + entry2)
            return
        count += 1
    print("Match!")
    return 

if __name__ == "__main__":
    tcl_list = read_csv('blobTest.csv')
    sequence = "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA"
    blobbed = Blobulator(sequence, .4, 4)
    blobbed_sequence = blobbed.get_domain()
    tcl_blob_list = convert_to_blob_type(tcl_list)
    compare_lists(blobbed_sequence, tcl_blob_list)

