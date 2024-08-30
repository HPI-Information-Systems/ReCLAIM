import math
from rdflib import Graph, URIRef, Literal, RDF
import pandas as pd
from .helpers import keys_to_camel_case
from . import uris


class Record:
    def __init__(self, source_id: str, collection_id: str, record_id: str, data: dict):
        self.source_id = source_id
        self.collection_id = collection_id
        self.record_id = record_id
        self.data = keys_to_camel_case(data)

    def uri(self) -> str:
        return uris.raw(self.source_id, self.collection_id + "_" + self.record_id)

    def get_record_id(self) -> str:
        return self.record_id

    def get_source_id(self) -> str:
        return self.source_id

    def to_graph(self) -> Graph:
        '''Converts the record to a graph.
        The subgraph can be added to the main graph.'''
        graph = Graph()

        graph.add((URIRef(self.uri()), RDF.type, URIRef(uris.schema("Record"))))

        for key, value in self.data.items():
            if pd.isna(value):
                continue

            triple = (
                URIRef(self.uri()),
                URIRef(uris.raw(self.source_id, key)),
                Literal(value),
            )
            graph.add(triple)

        return graph

    def __getitem__(self, item):
        if item not in self.data:
            return None

        value = self.data[item]

        if pd.isna(value):
            return None

        return value
