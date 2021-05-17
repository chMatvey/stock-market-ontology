import csv

from src.data.metrics import all_metrics
from src.data.read_interim_data import read_interim_data
from src.data.risk_calculation import calculate_risk_and_expect_growth_in_month

stocks = read_interim_data()

# Write data to final CSV file
file = open('../../data/data.csv', 'w')
writer = csv.writer(file)
delimiter = ','
writer.writerow(['Ticker'] + all_metrics + ['Expect Growth in month', 'Risk'])

allParsedStocks = len(stocks)
noTinkoff = 0

for stock in stocks:
    ticker = stock['Ticker']
    values = [ticker]
    for metric in all_metrics:
        values.append(stock[metric])

    risk_and_growth = calculate_risk_and_expect_growth_in_month(ticker)
    print('Parsed ticker', ticker)
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
print('All parsed stocks:', allParsedStocks)
print('Accepted and saved:', allParsedStocks - noTinkoff)
print('Not included in Tinkoff store:', noTinkoff)