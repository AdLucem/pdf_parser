"""Extract all tables from an html file, printing and saving each to csv file."""

import pandas as pd

df_list = pd.read_html('../ipms_reader_manual.html')

for i, df in enumerate(df_list):
    print df
    df.to_csv('table {}.csv'.format(i))