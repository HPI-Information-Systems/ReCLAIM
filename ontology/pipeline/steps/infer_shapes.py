from rdflib import Graph, URIRef, RDF, BNode, Namespace, Literal, IdentifiedNode

from ..error import BuildError

JDCRP_SCHEMA = Namespace("https://graph.jdcrp.org/schema#")
JDCRP_SHAPES = Namespace("https://graph.jdcrp.org/shapes#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SHACL = Namespace("http://www.w3.org/ns/shacl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# This dictionary defines the ontology relations that can occur multiple times on one entity.
max_cardinality_overrides = {
    JDCRP_SCHEMA["subMaterialOf"]: None,
    JDCRP_SCHEMA["subClassificationOf"]: None,
    JDCRP_SCHEMA["consistsOfMaterial"]: None,
    JDCRP_SCHEMA["classifiedAs"]: None,
    JDCRP_SCHEMA["depictedInImage"]: None,
    JDCRP_SCHEMA["referencedInCardImage"]: None,
    JDCRP_SCHEMA["referencedInCardImageFront"]: None,
    JDCRP_SCHEMA["referencedInCardImageBack"]: None,
    JDCRP_SCHEMA["withInvolvementOf"]: None,
    JDCRP_SCHEMA["byLegalEntitiy"]: None,
    JDCRP_SCHEMA["identifiedBy"]: None,
    JDCRP_SCHEMA["possessor"]: None,
    JDCRP_SCHEMA["possessorBefore"]: None,
    JDCRP_SCHEMA["possessorAfter"]: None,
    JDCRP_SCHEMA["depositedBy"]: None,
    JDCRP_SCHEMA["fromLegalEntity"]: None,
    JDCRP_SCHEMA["fromCollection"]: None,
    JDCRP_SCHEMA["throughLegalEntity"]: None,
}

# This dictionary defines the minimum cardinality for the included ontology properties. The rest is optional.
min_cardinality_overrides = {
    JDCRP_SCHEMA["url"]: 1,
    JDCRP_SCHEMA["relativeOrder"]: 1,
}

# Type inference is not attempted for URIs in this list. For example, the wikidataUri doesn't reference a
# jdcrp:Entity URI or a primitive XSD datatype, and thus cannot be inferred.
arbitrary_type_properties = [JDCRP_SCHEMA["wikidataUri"]]


def run(graph: Graph):
    """
    The single source of truth for our ontology are the turtle files in ontology/src.
    In order to validate ETL output against this ontology, in addition to the RDF schema, we need SHACL shapes.
    This script infers SHACL shapes automatically from the RDF schema and includes them in
    ontology/dist/combined_schema.ttl.

    Note, that the input of this method is NOT the output of ETL scripts, but rather the graph of the RDF schema itself.
    """
    for entity_uri in inferable_entity_uris(graph):
        infer_shape(graph, entity_uri)


def infer_shape(graph: Graph, target_uri: URIRef):
    # Derive the shapes URI from the target entities URI, e.g. CulturalAsset -> CulturalAssetShape
    target_name = target_uri.split("#")[1]
    shape_uri = JDCRP_SHAPES[target_name + "Shape"]

    graph.add((shape_uri, RDF.type, SHACL.NodeShape))
    graph.add((shape_uri, SHACL.targetClass, target_uri))

    # Make sure that the shape is closed, i.e. no additional properties are allowed
    graph.add((shape_uri, SHACL.closed, Literal(True)))

    # As the shape is closed, validation will complain about the type property.
    # As it is not explicitly mentioned in our inferred shapes, we need to ignore it.
    ignored_list = make_shacl_list(graph, [RDF.type])
    graph.add((shape_uri, SHACL.ignoredProperties, ignored_list))

    for property_uri in inferable_property_uris(graph, target_uri):
        blank_node = infer_property(graph, property_uri)
        graph.add((shape_uri, SHACL.property, blank_node))


def infer_property(graph: Graph, property_uri: URIRef) -> BNode:
    property_shape_node = BNode()
    graph.add((property_shape_node, SHACL.path, property_uri))

    # Default to making all properties optional, and allowing a single value
    min_cardinality = min_cardinality_overrides.get(property_uri, 0)
    max_cardinality = max_cardinality_overrides.get(property_uri, 1)

    if min_cardinality is not None:
        graph.add((property_shape_node, SHACL.minCount, Literal(min_cardinality)))
    if max_cardinality is not None:
        graph.add((property_shape_node, SHACL.maxCount, Literal(max_cardinality)))

    # Get the attributes of the RDF property as a dict, e.g. rdfs:domain, rdfs:range
    attributes = attributes_of_uri(graph, property_uri)

    if str(RDFS.range) not in attributes:
        # We cannot infer the shape of a property without a range given.
        # Unless it is explicitly allowed to be of arbitrary type, raise an exception.
        if property_uri in arbitrary_type_properties:
            return property_shape_node

        raise BuildError(
            "Cannot infer shape for " + str(property_uri),
            "No range specified for property",
            warning=True,
        )

    range_uri = URIRef(attributes[str(RDFS.range)])

    if range_uri in XSD:
        graph.add((property_shape_node, SHACL.datatype, range_uri))

    elif range_uri in JDCRP_SCHEMA:
        class_constraints = []

        # sh:class constraints don't support inheritance. E.g. jdcrp:LegalEntity has the subclass jdcrp:Person.
        # SHACL would not allow a property constrainted to jdcrp:LegalEntity to reference a jdcrp:Person.
        # Therefore, we determine all subclasses and also list them as possible classes for the property.
        for subclass_uri in get_self_and_subclasses_of(graph, range_uri):
            class_constraint = BNode()
            graph.add((class_constraint, SHACL["class"], subclass_uri))
            class_constraints.append(class_constraint)

        if len(class_constraints) > 0:
            graph.add(
                (
                    property_shape_node,
                    SHACL["or"],
                    make_shacl_list(graph, class_constraints),
                )
            )

    else:
        raise BuildError(
            "Cannot infer shape for " + str(property_uri),
            "Range "
            + str(range_uri)
            + " is not an XSD datatype, a JDCRP entity, nor allow-listed for arbitrary type.",
            warning=True,
        )

    return property_shape_node


def inferable_entity_uris(graph: Graph) -> list[URIRef]:
    """
    Returns the URIs of all entities of which a shape can be inferred (all subclasses of jdcrp:Entity).
    """
    result = graph.query(
        """
        SELECT ?s WHERE {{
            {{ ?s rdfs:subClassOf* jdcrp:Entity }}
        }}
    """
    )

    for row in result:
        assert isinstance(row[0], URIRef)
        yield row[0]


def inferable_property_uris(graph: Graph, entity_uri: URIRef) -> list[URIRef]:
    result = graph.query(
        f"""
        SELECT ?property
        WHERE {{
            <{entity_uri}> rdfs:subClassOf* ?class .
            ?property rdf:type rdf:Property ;
                      rdfs:domain ?class .
        }}
    """
    )

    for row in result:
        assert isinstance(row[0], URIRef)
        yield row[0]


def attributes_of_uri(graph: Graph, uri: URIRef) -> dict:
    """
    Generic helper to return all attributes of a given URI as a dict.
    """
    result = graph.query(
        f"""
        SELECT ?property ?value
        WHERE {{
          <{uri}> ?property ?value .
        }}
    """
    )

    return {str(key): str(value) for key, value in result}


def get_self_and_subclasses_of(graph: Graph, uri: URIRef) -> list[URIRef]:
    result = graph.query(
        f"""
        SELECT ?s WHERE {{
            {{ ?s rdfs:subClassOf* <{uri}> }}
        }}
    """
    )

    for row in result:
        assert isinstance(row[0], URIRef)
        yield row[0]


def make_shacl_list(graph: Graph, list_items: list[IdentifiedNode]) -> URIRef | BNode:
    """
    In SHACL, lists are implemented as linked lists. This helper creates a linked list of the given nodes.
    As a base case, we terminate the list with RDF.nil.
    """
    if len(list_items) == 0:
        return RDF.nil

    list_node = BNode()
    graph.add((list_node, RDF.first, list_items[0]))
    graph.add((list_node, RDF.rest, make_shacl_list(graph, list_items[1:])))

    return list_node
