import string

from rdflib import Graph, Literal
from rdflib.namespace import RDF

from src.ontology.data_reader import get_companies_sectors_countries, get_stocks
from src.ontology.entities import *


def default_data_parser(value):
    return value


def percent_data_parser(value):
    return value.replace('%', '')


def default_name_parser(name):
    return name.strip()


def to_fixed(number, digits=2):
    return f"{number:.{digits}f}"


dataPropertyMap = {
    'P/E': {
        'relation': hasPE,
        'data_parser': default_data_parser
    },
    'P/S': {
        'relation': hasPS,
        'data_parser': default_data_parser
    },
    'Dividend %': {
        'relation': hasAverageDividendYield,
        'data_parser': percent_data_parser
    },
    'Payout': {
        'relation': hasPayoutRatio,
        'data_parser': percent_data_parser
    },
    'Beta': {
        'relation': hasBeta,
        'data_parser': percent_data_parser
    },
    'Expect Growth in month': {
        'relation': hasExpectGrowthInMonth,
        'data_parser': to_fixed
    },
    'Risk': {
        'relation': hasRisk,
        'data_parser': to_fixed
    }
}


def add_indexes(graph: Graph):
    indexes = ['DJIA', 'S&P500']
    return add_class_individuals_to_graph(graph, Index, indexes)


def add_companies_sectors_countries(graph: Graph):
    companies, sectors, countries = get_companies_sectors_countries()

    companiesResult = add_class_individuals_to_graph(graph, Company, companies, lambda name: name.replace(',', '') \
                                                     .replace('.', '') \
                                                     .strip())
    sectorsResult = add_class_individuals_to_graph(graph, Sector, sectors)
    countriesResult = add_class_individuals_to_graph(graph, Country, countries)

    return companiesResult, sectorsResult, countriesResult


def add_stocks(graph: Graph, all_indexes_nodes, all_companies_nodes, all_sectors_nodes, all_countries_nodes):
    stocks = get_stocks()

    result = {}
    for stock in stocks:
        ticker = stock['Ticker']
        stock_node = add_class_individual_to_graph(graph, Stock, ticker)
        result[ticker] = stock_node

        # Set object properties
        company_node = all_companies_nodes[stock['Name']]
        sector_node = all_sectors_nodes[stock['Sector']]
        country_node = all_countries_nodes[stock['Country']]
        indexes_nodes = get_indexes_nodes_for_stock(stock['Index'], all_indexes_nodes)

        add_object_property(graph, stock_node, company_node, hasCompany)
        add_object_property(graph, stock_node, sector_node, includeInSector)
        add_object_property(graph, stock_node, country_node, hasCountry)
        for index_node in indexes_nodes:
            add_object_property(graph, stock_node, index_node, includeInIndex)

        # Set data properties
        for key in dataPropertyMap.keys():
            dataPropertyInfo = dataPropertyMap[key]
            value = stock[key]
            if value == '-':
                continue
            parsed_value = dataPropertyInfo['data_parser'](value)
            add_data_property(graph, stock_node, parsed_value, dataPropertyInfo['relation'])

    return result


def add_class_individuals_to_graph(graph: Graph, Class: URIRef, names: list[string], parser=default_name_parser):
    result = {}
    for name in names:
        result[name] = add_class_individual_to_graph(graph, Class, name, parser)

    return result


def add_class_individual_to_graph(graph: Graph, Class: URIRef, name: string, parser=default_name_parser):
    parsed_name = parser(name)
    individual = to_URIRef(parsed_name.replace(' ', '_'))
    triple = (individual, RDF.type, Class)
    graph.add(triple)

    return individual


def add_object_property(graph, domain, client, relation):
    triple = (domain, relation, client)
    graph.add(triple)


def add_data_property(graph, domain, value, relation):
    triple = (domain, relation, Literal(value, datatype='xsd:float'))
    graph.add(triple)


def get_indexes_nodes_for_stock(stock_indexes: string, all_indexes_nodes):
    if stock_indexes == '-':
        return []

    parsed_stock_indexes = stock_indexes.replace(' ', '')

    result = []
    for key in all_indexes_nodes.keys():
        if key in parsed_stock_indexes:
            result.append(all_indexes_nodes[key])

    return result
