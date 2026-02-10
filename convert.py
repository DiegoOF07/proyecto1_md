#Con esto se unifican todos los archivos de 10 años en un solo archivo 
# csv para facilitar su manejo

import pandas as pd
from glob import glob

files = glob("./data/spss/defun_*.sav")
dfs = []

for file in files:
    df = pd.read_spss(file)
    dfs.append(df)


df = pd.read_spss("./data/spss/defun_2022.sav")
print(df.info())
print(df.head())

df_total = pd.concat(dfs, ignore_index=True)

df_total.to_csv("./data/csv/defun_2012_2022.csv", index=False)