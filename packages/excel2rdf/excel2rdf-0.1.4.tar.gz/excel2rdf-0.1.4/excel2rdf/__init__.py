from rdflib import Graph, URIRef, Literal, Namespace
import pandas as pd
import validators

from uuid import uuid4
import re


def is_curie(value):
    return re.fullmatch('\\S+:\\S+', value)


def _get_prefixes(df):
    prefixes = dict()
    base_uri = None
    g = Graph()

    for i, row in df.iterrows():
        if row.values[0].strip() == '#':
            prefixes.update({row.values[1]: row.values[2]})
            g.bind(row.values[1], Namespace(row.values[2]))
        elif row.values[0].strip() == '##':
            base_uri = row.values[1]

    return base_uri, prefixes, g


def _resolve_curie(curie, prefixes):
    try:
        prefix, localname = curie.split(':')
    except Exception as e:
        raise Exception(str(e), curie)
    if not prefixes.get(prefix):
        raise Exception(f'Prefix {prefix} is not defined.')
    return URIRef(prefixes[prefix] + localname)


def _generate_uri(base_uri):
    return URIRef(base_uri + str(uuid4()))


def _add_object(value, prefixes):
    if not pd.isnull(value) and type(value) == str and value.__contains__(':'):
        if validators.url(value):
            return URIRef(value)
        elif is_curie(value):
            return _resolve_curie(value, prefixes)

    return Literal(value)


def convert(df, base_uri, prefixes):
    g = Graph()

    for i, row in df.iterrows():
        uri = URIRef(row.uri) if not pd.isnull(row.uri) else _generate_uri(base_uri)

        for key in row.keys():
            if key != 'uri':
                if not pd.isnull(row[key]):
                    g.add((uri, _resolve_curie(key, prefixes), _add_object(row[key], prefixes)))

    return g


def excel2rdf(file):
    prefixes_df = pd.read_excel(file, header=None, sheet_name='prefixes')
    base_uri, prefixes, prefixes_g = _get_prefixes(prefixes_df)
    df = pd.read_excel(file, sheet_name=0)
    g = convert(df, base_uri, prefixes) + prefixes_g

    return g