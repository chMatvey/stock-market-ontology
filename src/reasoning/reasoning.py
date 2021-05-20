from owlready2 import *

ontology = get_ontology('../../Stock-market-ontology3.rdf')
ontology.load()

with ontology:
    sync_reasoner()

ontology.save(file="result.rdf", format="rdfxml")

