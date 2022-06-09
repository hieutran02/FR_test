import csv
from csv import reader
import os
from dotenv import load_dotenv

load_dotenv()
TP = 0
FN = 0
FP = 0
count = 0
#Calculate stats
with open('{}.csv'.format(os.environ.get('FILE')), 'r') as file1, open('result/result_{}.csv'.format(os.environ.get('FILE')), 'r') as file2:
    reader1 = reader(file1)
    row1 = next(reader1)
    reader2 = reader(file2)
    row2 = next(reader2)
    while True:
        try:
            for i in range (min(len(row1), len(row2))):
                if row1[i] != row2[i]:
                    print (row2[i])
                    if row2[i] != '':
                        FP += 1
                    else:
                        FN += 1
                else:
                    TP += 1
            if len(row1) > len(row2):
                diff = len(row1) - len(row2)
                FN += sum(1 for e in row1[-diff:] if e)
            elif len(row1) < len(row2):
                diff = - len(row1) + len(row2)
                FP += sum(1 for e in row2[-diff:] if e)
            row1 = next(reader1)
            row2 = next(reader2)
        except StopIteration:
            break

precision = TP/(TP + FP)
recall = TP/(TP + FN)
F1_score = 2 * precision * recall /(precision + recall)
print ("precision: {}, recall : {}, F1_score: {}".format(precision, recall, F1_score))
    