import pandas as pd
from rdflib import Graph

from src.ontology.entities import to_URIRef
from src.queries.queries import most_growing_stocks_query, most_growing_stocks_in_sector_query, \
    most_growing_stocks_in_index_query, most_dividend_paying_stocks_query

graph = Graph()
graph.parse('../../Stock-market-ontology.rdf', format='n3')


def run_query(query):
    result = graph.query(query)
    return pd.DataFrame(result, columns=result.vars)


most_growing_stocks = run_query(most_growing_stocks_query(max_risk=8, max_pe=35))

sector1 = 'Technology'
most_growing_stocks_in_sector1 = run_query(most_growing_stocks_in_sector_query(sector1))

sector2 = 'Communication_Services'
most_growing_stocks_in_sector2 = run_query(most_growing_stocks_in_sector_query(sector2))

index = 'S&P500'
most_growing_stocks_in_index = run_query(most_growing_stocks_in_index_query(index))

most_dividend_paying_stocks = run_query(most_dividend_paying_stocks_query())

print('The most growing stocks:')
print(most_growing_stocks)
print()

print("""The most growing stocks in %s sector: """ % sector1)
print(most_growing_stocks_in_sector1)
print()

print("""The most growing stocks in %s sector: """ % sector2)
print(most_growing_stocks_in_sector2)
print()

print("""The most growing stocks in %s index: """ % index)
print(most_growing_stocks_in_index)
print()

print('The dividend paying stocks:')
print(most_dividend_paying_stocks)
print()