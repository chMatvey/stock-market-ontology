from rdflib import Graph
from rdflib.void import generateVoID

graph = Graph()
graph.parse('../../Stock-market-ontology.rdf', format='n3')

a = generateVoID(graph)
a[0].serialize(destination='result.rdf')

