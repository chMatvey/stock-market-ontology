import csv

import pandas as pd

from src.data.data_parser import get_fundamental_data, get_stock_ticker_list
from src.data.risk_calculation import calculate_risk_and_expect_growth_in_month
from src.data.metrics import all_metrics


# Parse data from resource
source_file_name = '../../data/nasdaq_screener_1620853648876.csv'  # Replace on your own file
stock_ticker_list = get_stock_ticker_list(source_file_name, 'Symbol')
df = pd.DataFrame(index=stock_ticker_list)
[df, notFound] = get_fundamental_data(df)


# Write data to interim CSV file
file = open('../../data/data_interim.csv', 'w')
writer = csv.writer(file)
delimiter = ','
writer.writerow(['Ticker'] + all_metrics)

for ticker in df.index:
    if ticker in notFound:
        continue
    if df.loc[ticker, 'P/E'] == '-':  # Skip if P/E empty
        continue

    values = [ticker]
    for metric in all_metrics:
        values.append(df.loc[ticker, metric])
    writer.writerow(values)

file.close()
print('Saved interim CSV')


# Write data to final CSV file
file = open('../../data/data.csv', 'w')
writer = csv.writer(file)
delimiter = ','
writer.writerow(['Ticker'] + all_metrics + ['Expect Growth in month', 'Risk'])

allStocks = len(stock_ticker_list)
notFoundStocks = 0
noPEStocks = 0
noTinkoff = 0

for ticker in df.index:
    if ticker in notFound:
        notFoundStocks += 1
        continue
    if df.loc[ticker, 'P/E'] == '-':  # Skip if P/E empty
        noPEStocks += 1
        continue

    values = [ticker]
    for metric in all_metrics:
        values.append(df.loc[ticker, metric])

    risk_and_growth = calculate_risk_and_expect_growth_in_month(ticker)
    print('Parsed ticker via Tinkoff:', ticker)
    if risk_and_growth is None:
        noTinkoff += 1
        continue
    [expect_growth, risk] = risk_and_growth
    values.append(expect_growth)
    values.append(risk)

    writer.writerow(values)

file.close()
print('Saved final CSV')


# Result statistics
print('All stocks:', allStocks)
print('Accepted and saved:', allStocks - notFoundStocks - noPEStocks - noTinkoff)
print('Not found:', notFoundStocks)
print('Without PE:', noPEStocks)
print('Not included in Tinkoff store:', noTinkoff)
