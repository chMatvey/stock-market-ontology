import pandas as pd


def get_companies_sectors_countries(file_name='../../data/data.csv', separator=','):
    table = pd.read_csv(file_name, sep=separator, parse_dates=[
        'Name', 'Sector', 'Country'
    ])

    allCompanies = set()
    allSectors = set()
    allCountries = set()

    for company in table['Name']:
        allCompanies.add(company)

    for sector in table['Sector']:
        allSectors.add(sector)

    for country in table['Country']:
        allCountries.add(country)

    return list(allCompanies), list(allSectors), list(allCountries)


def get_stocks(file_name='../../data/data.csv', separator=','):
    stocks = []
    table = pd.read_csv(file_name, sep=separator)
    for row in table.iterrows():
        stock = {}
        for col in table.columns:
            stock[col] = row[1][col]
        stocks.append(stock)

    return stocks
