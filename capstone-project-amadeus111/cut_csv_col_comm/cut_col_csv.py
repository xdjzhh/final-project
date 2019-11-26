import pandas as pd


filename='comm.csv'

data = pd.read_csv(filename)
col_name=data.columns.values.tolist()


for item in col_name:
    data[[item]].to_csv(f'{item}.csv',index=False)
