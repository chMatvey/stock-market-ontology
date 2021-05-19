from rdflib import Graph

from src.ontology.ontology_aggregator import add_indexes, add_companies_sectors_countries, add_stocks

graph = Graph()
graph.parse('../../Stock-market-ontology.owl')

indexes = add_indexes(graph)
companies, sectors, countries = add_companies_sectors_countries(graph)
add_stocks(graph, indexes, companies, sectors, countries)

graph.serialize(destination='../../Stock-market-ontology.rdf', format='n3')