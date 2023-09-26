import os
import pandas as pd
# open csv as dataframe
df = pd.read_csv('./matein.csv', sep=',', header=0)
print(df.keys())

rating = df.loc[:,' rating']
print(rating.describe())

print(df[df[' rating'] > 2200])