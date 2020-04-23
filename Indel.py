import numpy as np
import pandas as pd
import sys
import re
from collections import Counter


# The code takes:
# Pileup_sorted, prefix

total_data_read_file = sys.argv[1]
prefix = sys.argv[2]


total_data = pd.read_csv("%s" % total_data_read_file, header=None, sep='\t',
                         dtype={0: str, 1: int,
                                2: str, 3: int, 4: str, 5: str})

sequence = total_data[4]
position = total_data[1]
indel_matrix = np.zeros((len(total_data), 10), dtype=object)
del_histogram = np.zeros((len(total_data), 3), dtype=object)

for row_number in range(len(total_data)):
    a = sequence[row_number]
    del_type = re.findall('-[0-9]+[ACGTNacgtn]+', a, flags=0)
    del_type_total = len(del_type)
    del_type_count = Counter(del_type)
    indel_matrix[row_number][0] = position[row_number]
    indel_matrix[row_number][1] = total_data[3][row_number]

    indel_matrix[row_number][4] = del_type_total
    indel_matrix[row_number][5] = float(float(del_type_total) / total_data[3][row_number]) * 100
    indel_matrix[row_number][6] = del_type_count.most_common()

    ins = re.findall('\+[0-9]+[ACGTNacgtn]+', a, flags=0)
    ins_total = len(ins)
    ins_count = Counter(ins)
    indel_matrix[row_number][7] = ins_total
    indel_matrix[row_number][8] = float(float(ins_total) / total_data[3][row_number]) * 100
    indel_matrix[row_number][9] = ins_count.most_common()

    dele = re.findall('\*', a, flags=0)
    dele_total = len(dele)
    del_histogram[row_number][0] = position[row_number]
    del_histogram[row_number][1] = dele_total
    del_histogram[row_number][2] = float(float(dele_total) / total_data[3][row_number]) * 100

    indel_matrix[row_number][2] = del_type_total + ins_total
    indel_matrix[row_number][3] = float(float(del_type_total + ins_total) / total_data[3][row_number]) * 100

Columns = ["Position", "Coverage", "Total Indels", "%Indels", "Total Deletions", "%Deletions", "Type of Deletions",
           "Total Insertions", "%Insertions", "Type of Insertions"]
InDel_matrix = pd.DataFrame(indel_matrix, columns=Columns)
InDel_matrix.to_csv("%s_InDel_Matrix.csv" % prefix, index=True, sep=' ')

Del_histo_Columns = ["Position", "Total Deletions", "%Deletions"]
Del_histo = pd.DataFrame(del_histogram, columns=Del_histo_Columns)
Del_histo.to_csv("%s_Del_Histogram.csv" % prefix, index=True, sep=' ')
