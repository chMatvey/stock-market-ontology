from rdflib import URIRef

URI = 'http://www.semanticweb.org/matvey/ontologies/2021/4/stock-market-ontology#'


def to_URIRef(param):
    result = URIRef(URI + param)
    return result


# Classes
Asset = to_URIRef('Asset')
Bond = to_URIRef('Bond')
Company = to_URIRef('Company')
Country = to_URIRef('Country')
Currency = to_URIRef('Currency')
Dividend = to_URIRef('Dividend')
Fond = to_URIRef('Fond')
Growth = to_URIRef('Growth')
Index = to_URIRef('Index')
Sector = to_URIRef('Sector')
Stock = to_URIRef('Stock')

# Object properties
hasCompany = to_URIRef('hasCompany')
hasCountry = to_URIRef('hasCountry')
hasCurrency = to_URIRef('hasCurrency')
includeInIndex = to_URIRef('includeInIndex')
includeInSector = to_URIRef('includeInSector')

# Data properties
hasAverageDividendYield = to_URIRef('hasAverageDividendYield')
hasPE = to_URIRef('hasPE')
hasPS = to_URIRef('hasPS')
hasPayoutRatio = to_URIRef('hasPayoutRatio')
hasExpectGrowthInMonth = to_URIRef('hasExpectGrowInMonth')
hasRisk = to_URIRef('hasRisk')
hasBeta = to_URIRef('hasBeta')
