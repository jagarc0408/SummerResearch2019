import csv
import pandas as pd

tsv = []
with open("FP_data.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        tsv.append(row)

entries = []    
for i in range(len(tsv)):
    entries.append(tsv[i])
        
#2,5,8
checking_majority = []
for i in range(0,len(entries)):
    classifications = []
    for j in range(len(entries[i])):
        if j == 2:
            classifications.append(entries[i][j])
        elif j == 5:
            classifications.append(entries[i][j])
        elif j == 8:
            classifications.append(entries[i][j])
    checking_majority.append(classifications)
    
#Getting Majority Yes or No's, 1st index is not relevant
majority_binary = []
for i in range(0,len(checking_majority)):
    yes_count = 0
    for j in checking_majority[i]:
        if j == 'Yes':
            yes_count += 1
        
    if yes_count >= 2:
        majority_binary.append(1)
    else:
        majority_binary.append(0)
