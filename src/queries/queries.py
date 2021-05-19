# Get the most growing stocks with moderate risks
from src.ontology.entities import URI


def most_growing_stocks_query(max_risk=8, max_pe=35, min_beta=0.59, max_beta=1.59):
    return """
        prefix : <http://www.semanticweb.org/matvey/ontologies/2021/4/stock-market-ontology#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?name ?company ?growth ?pe ?risk ?beta WHERE {
            ?stock rdf:type :Stock .
            ?stock :hasExpectGrowInMonth ?growth .
            ?stock :hasRisk ?risk .
            ?stock :hasPE ?pe .
            ?stock :hasCompany ?companyUri .
            ?stock :hasBeta ?beta .
            BIND(REPLACE(STR(?companyUri), "%s", "", "i") AS ?company) .
            BIND(REPLACE(STR(?stock), "%s", "", "i") AS ?name) .
            FILTER(
                xsd:float(STR(?risk)) <= %s &&
                xsd:float(STR(?pe)) <= %s
            ) .
            FILTER(                
                xsd:float(STR(?beta)) >= %s &&
                xsd:float(STR(?beta)) <= %s
            )
        }
        ORDER BY DESC(xsd:float(STR(?growth)))
        LIMIT 10
    """ % (URI, URI, max_risk, max_pe, min_beta, max_beta)


def most_growing_stocks_in_sector_query(sector, max_risk=8, max_pe=35, min_beta=0.59, max_beta=1.59):
    return """
        prefix : <http://www.semanticweb.org/matvey/ontologies/2021/4/stock-market-ontology#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?name ?sector ?company ?growth ?pe ?risk ?beta WHERE {
            ?stock rdf:type :Stock .
            ?stock :hasExpectGrowInMonth ?growth .
            ?stock :hasRisk ?risk .
            ?stock :hasPE ?pe .
            ?stock :hasCompany ?companyUri .
            ?stock :hasBeta ?beta .
            ?stock :includeInSector ?sectorUri .
            BIND(REPLACE(STR(?sectorUri), "%s", "", "i") AS ?sector) .
            BIND(REPLACE(STR(?companyUri), "%s", "", "i") AS ?company) .
            BIND(REPLACE(STR(?stock), "%s", "", "i") AS ?name) .
            FILTER(STR(?sector) = "%s") .
            FILTER(
                xsd:float(STR(?risk)) <= %s &&
                xsd:float(STR(?pe)) <= %s
            ) .
            FILTER(                
                xsd:float(STR(?beta)) >= %s &&
                xsd:float(STR(?beta)) <= %s
            )
        }
        ORDER BY DESC(xsd:float(STR(?growth)))
        LIMIT 10
    """ % (URI, URI, URI, sector, max_risk, max_pe, min_beta, max_beta)


def most_growing_stocks_in_index_query(index, max_risk=8, max_pe=35, min_beta=0.59, max_beta=1.59):
    return """
        prefix : <http://www.semanticweb.org/matvey/ontologies/2021/4/stock-market-ontology#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?name ?index ?company ?growth ?pe ?risk ?beta WHERE {
            ?stock rdf:type :Stock .
            ?stock :hasExpectGrowInMonth ?growth .
            ?stock :hasRisk ?risk .
            ?stock :hasPE ?pe .
            ?stock :hasCompany ?companyUri .
            ?stock :hasBeta ?beta .
            ?stock :includeInIndex ?indexUri .
            BIND(REPLACE(STR(?indexUri), "%s", "", "i") AS ?index) .
            BIND(REPLACE(STR(?companyUri), "%s", "", "i") AS ?company) .
            BIND(REPLACE(STR(?stock), "%s", "", "i") AS ?name) .
            FILTER(STR(?index) = "%s") .
            FILTER(
                xsd:float(STR(?risk)) <= %s &&
                xsd:float(STR(?pe)) <= %s
            ) .
            FILTER(                
                xsd:float(STR(?beta)) >= %s &&
                xsd:float(STR(?beta)) <= %s
            )
        }
        ORDER BY DESC(xsd:float(STR(?growth)))
        LIMIT 10
    """ % (URI, URI, URI, index, max_risk, max_pe, min_beta, max_beta)


def most_dividend_paying_stocks_query(min_dividend_percent=2, min_payout=30, max_payout=75,
                                      max_pe=35, min_beta=0.59, max_beta=1.59):
    return """
        prefix : <http://www.semanticweb.org/matvey/ontologies/2021/4/stock-market-ontology#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?name ?company ?dividend ?payout ?pe ?beta WHERE {
            ?stock rdf:type :Stock .
            ?stock :hasAverageDividendYield ?dividend .
            ?stock :hasPayoutRatio ?payout .
            ?stock :hasPE ?pe .
            ?stock :hasBeta ?beta .
            ?stock :hasCompany ?companyUri .
            BIND(REPLACE(STR(?companyUri), "%s", "", "i") AS ?company) .
            BIND(REPLACE(STR(?stock), "%s", "", "i") AS ?name) .
            FILTER(xsd:float(STR(?dividend)) >= %s) .
            FILTER(
                xsd:float(STR(?payout)) >= %s &&
                xsd:float(STR(?payout)) <= %s
            ) .
            FILTER(xsd:float(STR(?pe)) <= %s) .
            FILTER(                
                xsd:float(STR(?beta)) >= %s &&
                xsd:float(STR(?beta)) <= %s
            )
        }
        ORDER BY DESC(xsd:float(STR(?dividend)))
        LIMIT 10
    """ % (URI, URI, min_dividend_percent, min_payout, max_payout, max_pe, min_beta, max_beta)
