from csv_diff import load_csv, compare
import pandas as pd
import numpy as np


diff = compare(
    load_csv(open("lord_nelson_place.csv"), key = "Suite #"),
    load_csv(open("result/result_lord_nelson_place.csv"), key = "Suite #")
)
print(diff)
#Count non-zero value in the ground truth table
df = pd.read_csv('result/result_lord_nelson_place.csv', na_values='', keep_default_na=False)
not_nulls = np.count_nonzero(df.notnull().values)
changes = len(diff['changed'])
#True positivity
TP = not_nulls - changes
print("Precision is {}".format(TP/not_nulls))