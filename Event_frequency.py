import numpy as np
import pandas as pd
import sys
import re
from collections import Counter

# The code takes:
# Pileup_sorted, prefix, cut positions

total_data_read_file = sys.argv[1]
prefix = sys.argv[2]
cut_pos_1 = sys.argv[3]
cut_pos_2 = sys.argv[4]

total_data = pd.read_csv("%s" % total_data_read_file, header=None, sep='\t',
                         dtype={0: str, 1: int,
                                2: str, 3: int, 4: str, 5: str})

sequence = total_data[4]
position = total_data[1]

frec_histogram = np.empty((len(total_data), 3), dtype=object)
i = 0
end = int(cut_pos_2) - position[0]

for row_number in range(0, end + 5):
    a = sequence[row_number]
    event_type = re.findall('[-+][0-9]+[ACGTNacgtn]+', a, flags=0)
    event_type_total = len(event_type)
    event_type_count = Counter(event_type)
    common_type = event_type_count.most_common()
    dic = dict(common_type)
    for value in dic.values():
        per = round(float(float(value) / total_data[3][row_number]) * 100, 2)
        if per > 0.1:
            b = list(dic.keys())[list(dic.values()).index(value)]
            c = re.findall('[-+]+', b, flags=0)
            d = re.findall('[0-9]+', b, flags=0)
            e = int("".join(d))
            if str("".join(c)) == '-':
                if position[row_number] + e > int(cut_pos_1) - 5:
                    frec_histogram[i][0] = position[row_number]
                    frec_histogram[i][1] = list(dic.keys())[list(dic.values()).index(value)]
                    frec_histogram[i][2] = per
                    i += 1
            else:
                if int(cut_pos_2) + 5 > position[row_number] > int(cut_pos_1) - 5:
                    frec_histogram[i][0] = position[row_number]
                    frec_histogram[i][1] = list(dic.keys())[list(dic.values()).index(value)]
                    frec_histogram[i][2] = per
                    i += 1

Columns = ["Position", "Event", "%Event"]
Event_matrix = pd.DataFrame(frec_histogram, columns=Columns).dropna()
Event_matrix.to_csv("%s_Events_Frequency.csv" % prefix, index=True, sep=' ')
