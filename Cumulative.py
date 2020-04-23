import numpy as np
import pandas as pd
import sys
# import re
# from collections import Counter
import pysam

# The code takes:
# Reference Sequence Name
# Prefix
# 5' most Cut position  (position 1)
# 3' most Cut position (position 3)


ref_seq_name = sys.argv[1]
prefix = sys.argv[2]
cut_pos_1 = sys.argv[3]
cut_pos_2 = sys.argv[4]

samfile = pysam.AlignmentFile("%s_sorted_sample.bam" % prefix, "rb")

dele = np.ndarray((samfile.count(), 1), dtype=object)
i = 0
ins = np.ndarray((samfile.count(), 1), dtype=object)
j = 0
indel = np.ndarray((samfile.count(), 1), dtype=object)
k = 0
pileup = samfile.pileup(reference="%s" % ref_seq_name, start=int(cut_pos_1) - 1, stop=int(cut_pos_2) + 1,
                        truncate=True, max_depth=0, stepper="samtools", min_base_quality=40)

for column in pileup:
    for reads in column.pileups:
        alig = reads.alignment
        if alig.query_name not in dele:
            if reads.is_del:
                dele[i][0] = alig.query_name
                i += 1
                if alig.query_name not in indel:
                    indel[k][0] = alig.query_name
                    k += 1
            elif alig.query_name not in ins:
                a = reads.indel
                if a > 0:
                    ins[j][0] = alig.query_name
                    j += 1
                    if alig.query_name not in indel:
                        indel[k][0] = alig.query_name
                        k += 1
        elif alig.query_name not in ins:
            a = reads.indel
            if a > 0:
                ins[j][0] = alig.query_name
                j += 1
                if alig.query_name not in indel:
                    indel[k][0] = alig.query_name
                    k += 1

del_matrix = pd.DataFrame(dele).dropna()
del_nd = del_matrix.drop_duplicates()
total_dele = round(float(len(del_nd)) / float(samfile.count()) * 200, 3)


ins_matrix = pd.DataFrame(ins).dropna()
ins_nd = ins_matrix.drop_duplicates()
total_ins = round(float(len(ins_nd)) / float(samfile.count()) * 200, 3)

indel_matrix = pd.DataFrame(indel).dropna()
indel_nd = indel_matrix.drop_duplicates()
total_indel = round(float(len(indel_nd)) / float(samfile.count()) * 200, 3)

with open("%s_Cumulative" % prefix, "w+") as Indel_file:
    Indel_file.write("The cumulative disruptive deletion is")
    Indel_file.write("\t")
    Indel_file.write(str(total_dele))
    Indel_file.write("\n")
    Indel_file.write("The cumulative disruptive insertion is")
    Indel_file.write("\t")
    Indel_file.write(str(total_ins))
    Indel_file.write("\n")
    Indel_file.write("The cumulative disruption is")
    Indel_file.write("\t")
    Indel_file.write(str(total_indel))
