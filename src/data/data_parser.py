import csv
import requests
from bs4 import BeautifulSoup as bs

from src.data.metrics import fundamental_metrics


resourceUrl = 'https://finviz.com/quote.ashx'


def get_fundamental_metric(soup, metric=None):
    if metric is None:
        metric = fundamental_metrics
    # Search in table with fundamental metrics
    name_cell = soup.find(text=metric) # First search header cell
    value_cell = name_cell.find_next(class_='snapshot-td2') # Next search closest cell
    return value_cell.text


def get_name_sector_country(soup):
    table = soup.find(attrs={'data-testid': 'quote-data-content'})
    links = table.findAll(class_='tab-link')

    name = links[0].find('b').text
    sector = links[1].text
    country = links[3].text

    return [('Name', name), ('Sector', sector), ('Country', country)]


def get_fundamental_data(df):
    notFound = []
    for symbol in df.index:
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
            response = requests.get(resourceUrl + '?t=' + symbol, headers=headers)
            soup = bs(markup=response.content, features="html.parser")

            for metric in fundamental_metrics:
                metricValue = get_fundamental_metric(soup, metric)
                df.loc[symbol, metric] = metricValue

            name_sector_country = get_name_sector_country(soup)
            for field in name_sector_country:
                df.loc[symbol, field[0]] = field[1]
        except Exception as e:
            notFound.append(symbol)
        print('Parsed ticker:', symbol)

    return df, notFound


def get_stock_ticker_list(file_name, ticker_field_name):
    tickers = []
    with open(file_name, newline='') as file:
        reader = csv.DictReader(file, [ticker_field_name])
        for row in reader:
            ticker = row[ticker_field_name]
            tickers.append(ticker)
    return tickers[1:]