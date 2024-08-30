import os
from typing import Dict, List
from rdflib import XSD, Graph, Namespace, URIRef

jdcrp = Namespace("https://graph.jdcrp.org/schema#")
jdcrp_shapes = Namespace("https://graph.jdcrp.org/shapes#")
sh = Namespace("http://www.w3.org/ns/shacl#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = XSD._NS


class PropertyRange:
    """
    Represents a single range (i.e. type) of a property.
    Consists of the URI of the property range, whether it is an entry type containing raw and parsed values, and whether it is a literal.
    """

    def __init__(self, range_uri: URIRef, is_entry: bool, is_literal: bool) -> None:
        self.range_uri = range_uri
        self.is_entry: bool = is_entry
        self.is_literal: bool = is_literal


class ClassProperty:
    """
    Contains the compound of ranges that make up a class property.
    Includes information about whether the property is optional and if it is a list.
    This is the final type of the property (e.g. Optional[List[Entry[str | int]]]).
    """

    def __init__(self, property_ranges: List[PropertyRange]) -> None:
        self.property_ranges = property_ranges
        self.is_optional: bool = False
        self.is_list: bool = False

    def all_ranges_are_literals(self) -> bool:
        """
        Returns true if all ranges of the property are literals.
        """
        return all(
            [structured_range.is_literal for structured_range in self.property_ranges]
        )


def get_all_classes(g: Graph, ignore_entity_types: List[URIRef]) -> list[URIRef]:
    """
    Get all class URIs from the schema file.
    """
    # Get all subjects (t[0]) from triples (g.triples) where the predicate is rdf:type and the object is rdfs:Class
    class_uris = []
    for t in g.triples((None, rdf.type, rdfs.Class)):
        class_uri = t[0]
        if class_uri not in ignore_entity_types:
            class_uris.append(class_uri)
    return class_uris


def get_all_superclasses(g: Graph, class_uri: str) -> List[URIRef]:
    """
    Get all superclasses of a class from the schema file.
    """

    superclasses = []
    inheritances = list(g.triples((None, rdfs.subClassOf, None)))
    for inheritance in inheritances:
        subclass = inheritance[0]
        superclass = inheritance[2]
        if subclass == class_uri:
            superclasses.append(superclass)
            superclasses.extend(get_all_superclasses(g, superclass))
    return superclasses


def get_all_subclasses(g: Graph, class_uri: str) -> List[URIRef]:
    """
    Get all subclasses of a class from the schema file.
    """

    subclasses = []
    inheritances = list(g.triples((None, rdfs.subClassOf, None)))
    for inheritance in inheritances:
        subclass = inheritance[0]
        superclass = inheritance[2]
        if superclass == class_uri:
            subclasses.append(subclass)
            subclasses.extend(get_all_subclasses(g, subclass))
    return subclasses


def get_structured_property_ranges(
    graph: Graph,
    property_uri: URIRef,
    property_ranges: List[URIRef],
    ignore_entity_types: List[URIRef],
    nonentry_properties: List[URIRef],
) -> List[PropertyRange]:
    """
    Parses properties as a list of structured PropertyRange objects.
    This function determines whether a given property is a literal, and whether it is an entry.

    :param property_name: The name of the property
    :param property_ranges: List of all possible types of the property's values. Example: Let property_uri be "jdcrp.firstName", then property_ranges is likely "[xsd:string]".
    """

    if not property_ranges:
        print(
            "Information: Property "
            + str(property_uri)
            + " has no given type for its value. Using xsd:string."
        )
        return [PropertyRange(xsd.string, is_entry=True, is_literal=True)]

    structured_property_ranges = []

    # Contains all ranges which are nonliterals, i.e., class types.
    # These class types can inherit from parent classes which must be added as well.
    # To ensure we do not add duplicate classes, use a set to collect the unique class property ranges first.
    class_property_ranges = set()

    for range_uri in property_ranges:
        if range_uri.startswith(xsd):
            structured_property_ranges.append(
                PropertyRange(
                    range_uri,
                    is_entry=(property_uri not in nonentry_properties),
                    is_literal=True,
                )
            )
        else:
            class_property_ranges.add(range_uri)
            for superclass in get_all_subclasses(graph, range_uri):
                class_property_ranges.add(superclass)

    for class_property_range in class_property_ranges:
        if class_property_range in ignore_entity_types:
            continue
        structured_property_ranges.append(
            PropertyRange(class_property_range, is_entry=False, is_literal=False)
        )

    return structured_property_ranges


def copy_inherited_properties(
    g: Graph,
    class_uris: List[str],
    properties_dict: Dict[str, Dict[str, ClassProperty]],
) -> None:
    """
    Copies all properties from superclasses to their subclasses recursively in the properties_dict in place.

    :param class_uris: List of all class URIs
    :param properties_dict: Dictionary of class properties to modify
    """

    for base_class in class_uris:
        for superclass in get_all_superclasses(g, base_class):
            if superclass not in properties_dict:
                continue

            if base_class not in properties_dict:
                properties_dict[base_class] = {}
            for property_name, property_class_obj in properties_dict[
                superclass
            ].items():
                if property_name not in properties_dict[base_class]:
                    properties_dict[base_class][property_name] = property_class_obj


def apply_shacl_constraints(
    g: Graph,
    class_uris: List[str],
    properties_dict: Dict[str, Dict[str, ClassProperty]],
    ignore_properties: List[URIRef],
) -> None:
    """
    Infers from the SHACL shapes whether properties are Optional or a List.
    Applies these constraints to the given properties_dict in place.

    :param g: Graph object containing the schema file
    :param class_uris: List of all class URIs
    :param properties_dict: Dictionary of class properties to modify
    :param ignore_properties: List of property uris to ignore
    """

    # For each class, get the NodeShape that corresponds to it
    # The Shacl Shapes are used to determine constraints (Optional, List)
    for class_uri in class_uris:
        if class_uri not in properties_dict:
            continue

        class_shape_uri = jdcrp_shapes[class_uri.removeprefix(jdcrp)] + "Shape"
        property_blank_nodes = list(g.triples((class_shape_uri, sh.property, None)))

        for property_node in property_blank_nodes:
            min_count = g.value(property_node[2], sh.minCount)
            max_count = g.value(property_node[2], sh.maxCount)
            attribute = g.value(property_node[2], sh.path)

            if attribute in ignore_properties:
                continue

            clean_attribute = attribute.removeprefix(jdcrp)
            if clean_attribute not in properties_dict[class_uri]:
                continue

            structured_property: ClassProperty = properties_dict[class_uri][
                clean_attribute
            ]

            if int(min_count) == 0:
                structured_property.is_optional = True

            if max_count == None or int(max_count) > 1:
                structured_property.is_list = True


def load_schema_file() -> Graph:
    """
    Load the schema turtle file from disk and parse it into a Graph object.
    """

    # Get the schema file path from the environment variable or from ontology dist directory
    schema_file = os.path.join(
        os.path.dirname(__file__), "..", "ontology", "dist", "combined_schema.ttl"
    )

    # Verify that the schema file exists
    if not os.path.exists(schema_file):
        raise FileNotFoundError(
            "Error: Schema file at "
            + schema_file
            + " could not be found. Place the schema file in the given path or set the SCHEMA_FILE_PATH environment variable."
        )

    # Parse the schema file
    g = Graph()

    try:
        g.parse(schema_file, format="ttl")
    except Exception as exception:
        raise exception(
            "Input ttl schema file "
            + schema_file
            + " could not be parsed. Please check if the file is valid."
        )

    return g


def get_structured_class_properties_from_ontology(
    ignore_properties: List[URIRef] = [],
    ignore_entity_types: List[URIRef] = [],
    nonentry_properties: List[URIRef] = [],
) -> Dict[str, Dict[str, ClassProperty]]:
    """
    Parses a structured dictionary of classes and their properties from the ontology schema file.
    """

    g = load_schema_file()
    class_uris = get_all_classes(g, ignore_entity_types)
    properties_dict: Dict[str, Dict[str, ClassProperty]] = {}

    property_triples = list(g.triples((None, rdf.type, rdf.Property)))
    for property in property_triples:
        if property[0] in ignore_properties:
            continue

        structured_ranges: List[PropertyRange] = get_structured_property_ranges(
            graph=g,
            property_uri=property[0],
            property_ranges=[t[2] for t in g.triples((property[0], rdfs.range, None))],
            ignore_entity_types=ignore_entity_types,
            nonentry_properties=nonentry_properties,
        )

        if len(structured_ranges) == 0:
            continue

        property_name = property[0].removeprefix(jdcrp)

        # Get all domains (classes which have the property)
        domains = list(g.triples((property[0], rdfs.domain, None)))
        if not domains:
            print(
                "Warning: Property " + property_name + " is not defined for any class."
            )
            continue

        # For each of its domains, append the StructuredProperty object to the domain's dictionary of properties
        for domain in domains:
            domain_uri = domain[2]

            if domain_uri not in class_uris:
                print(
                    "Warning: Class "
                    + str(domain_uri)
                    + " was given as a domain, but is not defined in the schema as a class or is defined as ignored. The class will be ignored."
                )
                continue

            if domain_uri not in properties_dict:
                properties_dict[domain_uri] = {}
            properties_dict[domain_uri][property_name] = ClassProperty(
                structured_ranges
            )

    # Add all inherited properties as own properties
    copy_inherited_properties(g, class_uris, properties_dict)

    # Determine whether properties are Optional or a List using the SHACL shapes
    apply_shacl_constraints(g, class_uris, properties_dict, ignore_properties)

    return properties_dict
