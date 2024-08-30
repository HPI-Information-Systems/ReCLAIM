from __future__ import annotations
import json
from rdflib import URIRef, RDF, Literal, Graph
from .record import Record
from . import uris


class Entity:
    def __init__(self, identifier: str, base_type: str, derived_from: Record):
        self.identifier = identifier
        self.base_type = base_type
        self.record = derived_from
        self.graph = Graph()
        self.derivation_mapping = {}

    def uri(self):
        return uris.entity(self.record.get_source_id(), self.base_type, self.identifier)

    def track_derivation(self, *, schema_attribute: str, raw_attribute: str):
        schema_attribute_uri = uris.schema(schema_attribute)
        raw_attribute_uri = uris.raw(self.record.get_source_id(), raw_attribute)

        if schema_attribute_uri not in self.derivation_mapping:
            self.derivation_mapping[schema_attribute_uri] = []

        if raw_attribute_uri in self.derivation_mapping[schema_attribute_uri]:
            return

        self.derivation_mapping[schema_attribute_uri].append(raw_attribute_uri)

    def literal(
        self, *, attribute: str, derived_using: str | list[str], datatype=None, **kwargs
    ):
        '''Add a literal value to the entity
        
        Args:
            attribute (str): the schema attribute to which the value should be added
            derived_using (str | list[str]): the raw attribute(s) from which the value should be derived
            value (str): the value to be added to the entity
            If the value is not provided, the value will be taken from the record as specified in derived_using 
        
        '''
        if "value" in kwargs:
            value = kwargs["value"]
        else:
            assert isinstance(
                derived_using, str
            ), "please provide an explicit value when deriving from multiple values"
            value = self.record[derived_using]

        if value is None:
            return

        if isinstance(derived_using, str):
            derived_using = [derived_using]

        triple = (
            URIRef(self.uri()),
            URIRef(uris.schema(attribute)),
            Literal(value, datatype=datatype),
        )

        for raw_attribute in derived_using:
            self.track_derivation(
                schema_attribute=attribute, raw_attribute=raw_attribute
            )

        self.graph.add(triple)

    def related(
        self,
        *,
        via: str,
        with_entity: Entity = None,
        with_entity_uri: str = None,
        inverse: bool = False,
        derived_using: str | list[str] = None,
    ):
        '''Add a relation to the entity'''
        assert (
            with_entity is None or with_entity_uri is None
        ), "please provide either an entity or a URI, not both"

        if with_entity is None and with_entity_uri is None:
            return

        if with_entity is not None:
            with_entity_uri = with_entity.uri()
            self.graph += with_entity.to_graph()

        if inverse:
            relation_triple = (
                URIRef(with_entity_uri),
                URIRef(uris.schema(via)),
                URIRef(self.uri()),
            )
        else:
            relation_triple = (
                URIRef(self.uri()),
                URIRef(uris.schema(via)),
                URIRef(with_entity_uri),
            )

        self.graph.add(relation_triple)

        if derived_using is None:
            derived_using = []
        elif isinstance(derived_using, str):
            derived_using = [derived_using]

        for raw_attribute in derived_using:
            self.track_derivation(schema_attribute=via, raw_attribute=raw_attribute)

    def to_graph(self) -> Graph:
        '''Returns the entity as a graph.
        This subgraph can be added to the main graph'''
        type_triple = (
            URIRef(self.uri()),
            RDF.type,
            URIRef(uris.schema(self.base_type)),
        )

        derived_from_triple = (
            URIRef(self.uri()),
            URIRef(uris.schema("derivedFrom")),
            URIRef(self.record.uri()),
        )

        derived_using_triple = (
            URIRef(self.uri()),
            URIRef(uris.schema("derivedUsingMapping")),
            Literal(json.dumps(self.derivation_mapping)),
        )

        self.graph.add(derived_from_triple)
        self.graph.add(derived_using_triple)
        self.graph.add(type_triple)

        return self.graph

    def __getitem__(self, attribute_name):
        attribute_uri = URIRef(uris.schema(attribute_name))

        query = f"""
            SELECT ?value
            WHERE {{
                <{self.uri()}> <{attribute_uri}> ?value.
            }}
        """

        result = self.graph.query(query)

        if result:
            for row in result:
                # Return first value found
                return row.value

        return None
