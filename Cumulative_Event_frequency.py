import numpy as np
import pandas as pd
import sys
import re

# The code takes:
# list of Event_Frequency.csv files
# Prefix

files = sys.argv[1]
prefix = sys.argv[2]

total_histogram = np.empty((1000000, 2), dtype=object)
total_histogram_Columns = ["Event", "%Event"]

line_counter = 0
for file in files:
    total_data = pd.read_csv(file, header=0, sep=' ',
                             dtype={0: int, 1: int,
                                    2: str, 3: float})

    sequence = total_data["Event"]
    weight = total_data["%Event"]
    frec_histogram = np.empty((len(total_data), 2), dtype=object)
    i = 0

    for row_number in range(len(total_data)):
        a = sequence[row_number]
        event_type = re.findall('[-+][0-9]+', a, flags=0)
        e = str("".join(event_type))
        frec_histogram[i][0] = e
        frec_histogram[i][1] = weight[row_number]
        i += 1
    frec_histogram = pd.DataFrame(frec_histogram).dropna()

    for line in range(len(frec_histogram)):
        total_histogram[line_counter][0] = frec_histogram[0][line]
        total_histogram[line_counter][1] = frec_histogram[1][line]
        line_counter += 1

total_data = pd.DataFrame(total_histogram, columns=total_histogram_Columns).dropna()

total_data = pd.DataFrame(total_data).sort_values(by="Event").reset_index(drop=True)
Event = total_data["Event"]
weight = total_data["%Event"]

ins_freq = np.empty((len(total_data), 3), dtype=object)
dele_freq = np.empty((len(total_data), 3), dtype=object)

i = 0
cumul_weight = 0
k = 0
Ins_Cumul = 0
ins_cumul_mean_freq = 0
dele_cumul_mean_freq = 0

for row_number in range(len(total_data) - 1):
    if "+" in Event[row_number]:
        ins_freq[i][0] = int("".join(Event[row_number]))
        if Event[row_number] == Event[row_number + 1]:
            k += 1
            ins_freq[i][1] = k
            cumul_weight = cumul_weight + weight[row_number]
            ins_freq[i][2] = cumul_weight
        else:
            k += 1
            ins_freq[i][1] = k
            cumul_weight = cumul_weight + weight[row_number]
            ins_freq[i][2] = cumul_weight
            cumul_weight = 0
            i += 1
            k = 0
    else:
        dele_freq[i][0] = abs(int("".join(Event[row_number])))
        if Event[row_number] == Event[row_number + 1]:
            k += 1
            dele_freq[i][1] = k
            cumul_weight = cumul_weight + weight[row_number]
            dele_freq[i][2] = cumul_weight
            if row_number == len(total_data) - 2:
                k += 1
                dele_freq[i][1] = k
                cumul_weight = cumul_weight + weight[row_number]
                dele_freq[i][2] = cumul_weight
        else:
            k += 1
            dele_freq[i][1] = k
            cumul_weight = cumul_weight + weight[row_number]
            dele_freq[i][2] = cumul_weight
            cumul_weight = 0
            i += 1
            k = 0

ins_total_data = pd.DataFrame(ins_freq).dropna().sort_values(by=0).reset_index(drop=True)
Event = ins_total_data[0]
Frequency = ins_total_data[1]
Weight_Freq = ins_total_data[2]
ins_cumul_freq = np.empty((len(ins_total_data), 5), dtype=object)
for row_number in range(len(ins_total_data)):
    ins_cumul_freq[row_number][0] = Event[row_number]
    ins_cumul_freq[row_number][1] = Frequency[row_number]
    Ins_Cumul = Ins_Cumul + ins_cumul_freq[row_number][1]
    ins_cumul_freq[row_number][2] = Ins_Cumul
    mean_freq = Event[row_number] * Frequency[row_number]
    ins_cumul_freq[row_number][3] = mean_freq
    ins_cumul_mean_freq = ins_cumul_mean_freq + mean_freq
    cumul_weight = cumul_weight + weight[row_number]
    ins_cumul_freq[row_number][4] = Weight_Freq[row_number]

Columns = ["Event", "Frequency", "Cumulative Frequency", "Mean Frequency", "Cumulative Weight"]
Ins_matrix = pd.DataFrame(ins_cumul_freq, columns=Columns)

ins_average = round(ins_cumul_mean_freq / Ins_Cumul, 2)
ins_q1 = round(25 / 100 * (Ins_Cumul + 1), 2)
ins_q2 = round(50 / 100 * (Ins_Cumul + 1), 2)
ins_q3 = round(75 / 100 * (Ins_Cumul + 1), 2)

for row_number in range(len(ins_cumul_freq) - 1):
    if ins_cumul_freq[row_number + 1][2] >= ins_q1 >= ins_cumul_freq[row_number][2]:
        Ins_Q1 = ins_cumul_freq[row_number + 1][0]
    elif ins_q1 <= ins_cumul_freq[0][2]:
        Ins_Q1 = ins_cumul_freq[0][0]
    if ins_cumul_freq[row_number + 1][2] >= ins_q2 >= ins_cumul_freq[row_number][2]:
        Ins_Q2 = ins_cumul_freq[row_number + 1][0]
    if ins_cumul_freq[row_number + 1][2] >= ins_q3 >= ins_cumul_freq[row_number][2]:
        Ins_Q3 = ins_cumul_freq[row_number + 1][0]


dele_total_data = pd.DataFrame(dele_freq).dropna().sort_values(by=0).reset_index(drop=True)
Event = dele_total_data[0]
Frequency = dele_total_data[1]
Weight_Freq = dele_total_data[2]
dele_cumul_freq = np.empty((len(dele_total_data), 5), dtype=object)
Dele_Cumul = 0
for row_number in range(len(dele_total_data)):
    dele_cumul_freq[row_number][0] = Event[row_number]
    dele_cumul_freq[row_number][1] = Frequency[row_number]
    Dele_Cumul = Dele_Cumul + dele_cumul_freq[row_number][1]
    dele_cumul_freq[row_number][2] = Dele_Cumul
    mean_freq = Event[row_number] * Frequency[row_number]
    dele_cumul_freq[row_number][3] = mean_freq
    dele_cumul_mean_freq = dele_cumul_mean_freq + mean_freq
    cumul_weight = cumul_weight + weight[row_number]
    dele_cumul_freq[row_number][4] = Weight_Freq[row_number]

Dele_matrix = pd.DataFrame(dele_cumul_freq, columns=Columns)

dele_average = round(dele_cumul_mean_freq / Dele_Cumul, 2)
dele_q1 = round(25 / 100 * (Dele_Cumul + 1), 2)
dele_q2 = round(50 / 100 * (Dele_Cumul + 1), 2)
dele_q3 = round(75 / 100 * (Dele_Cumul + 1), 2)

for row_number in range(len(dele_cumul_freq) - 1):
    if dele_cumul_freq[row_number + 1][2] >= dele_q1 > dele_cumul_freq[row_number][2]:
        Dele_Q1 = dele_cumul_freq[row_number + 1][0]
    if dele_cumul_freq[row_number + 1][2] >= dele_q2 > dele_cumul_freq[row_number][2]:
        Dele_Q2 = dele_cumul_freq[row_number + 1][0]
    if dele_cumul_freq[row_number + 1][2] >= dele_q3 > dele_cumul_freq[row_number][2]:
        Dele_Q3 = dele_cumul_freq[row_number + 1][0]

Cumulative_freq = pd.ExcelWriter("%s_Cumulative_Freq.xlsx" % prefix, engine="xlsxwriter")
Ins_matrix.to_excel(Cumulative_freq, sheet_name="Ins")
Dele_matrix.to_excel(Cumulative_freq, sheet_name="Del")

Stats_data = np.empty((8, 2), dtype=object)
Stats_data[0][0] = "The Average Insertion is"
Stats_data[0][1] = ins_average
Stats_data[1][0] = "The Median Insertion is"
Stats_data[1][1] = Ins_Q2
Stats_data[2][0] = "The Q1 Insertion is"
Stats_data[2][1] = Ins_Q1
Stats_data[3][0] = "The Q3 Insertion is"
Stats_data[3][1] = Ins_Q3
Stats_data[4][0] = "The Average Deletion is"
Stats_data[4][1] = dele_average
Stats_data[5][0] = "The Median Deletion is"
Stats_data[5][1] = Dele_Q2
Stats_data[6][0] = "The Q1 Deletion is"
Stats_data[6][1] = Dele_Q1
Stats_data[7][0] = "The Q3 Deletion is"
Stats_data[7][1] = Dele_Q3

Stats_data = pd.DataFrame(Stats_data)
Stats_data.to_excel(Cumulative_freq, sheet_name="Stats")
Cumulative_freq.save()
