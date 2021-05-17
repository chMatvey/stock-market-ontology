import csv

from src.data.metrics import all_metrics

source_file_name = '../../data/data_interim.csv'


def read_interim_data():
    stocks = []
    with open(source_file_name, newline='') as file:
        fields = ['Ticker'] + all_metrics
        reader = csv.DictReader(file, fields)
        for row in reader:
            stock = {}
            for field in fields:
                stock[field] = row[field]
            stocks.append(stock)
        file.close()

    return stocks[1:]