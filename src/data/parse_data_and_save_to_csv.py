import csv

import pandas as pd

from src.data.data_parser import get_fundamental_data, get_stock_ticker_list

# Parse data from resource
from src.data.metrics import all_metrics

sourceFileName = '../data/nasdaq_screener_1620853648876.csv' # Replace on your own file
stock_ticker_list = get_stock_ticker_list(sourceFileName, 'Symbol')
df = pd.DataFrame(index=stock_ticker_list)
result = get_fundamental_data(df)
df = result[0]
notFound = result[1]

# Write data to CSV file
file = open('../../data/data.csv', 'w')
writer = csv.writer(file)
delimiter = ','
writer.writerow(all_metrics)

for ticker in df.index:
    if ticker in notFound:
        continue
    values = []
    for metric in all_metrics:
        values.append(df.loc[ticker, metric])
    writer.writerow(values)
