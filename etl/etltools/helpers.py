import glob
import os
import re

from rdflib import Graph
from pyshacl import validate as _validate_shacl
from . import uris


def create_graph(source_id: str) -> Graph:
    """Creates a new graph and binds the necessary prefixes to it"""
    graph = Graph()

    graph.bind("jdcrp", uris.schema(""))
    graph.bind(f"raw_{source_id}", uris.raw(source_id, ""))
    graph.bind(
        f"{source_id}_CulturalAsset", uris.entity(source_id, "CulturalAsset", "")
    )
    graph.bind(f"{source_id}_Person", uris.entity(source_id, "Person", ""))
    graph.bind(f"{source_id}_Image", uris.entity(source_id, "Image", ""))
    graph.bind(f"{source_id}_Location", uris.entity(source_id, "Location", ""))
    graph.bind(f"{source_id}_Collection", uris.entity(source_id, "Collection", ""))
    graph.bind("material", uris.taxonomies("material", ""))
    graph.bind("classification", uris.taxonomies("classification", ""))
    return graph


def validate_graph(graph: Graph):
    """Validates the graph against the ontology schema.
    This function uses SHACL to validate the graph and outputs a file with the results if the graph does not conform to the schema"""
    graph += get_taxonomy_graph()

    shape_graph = get_shape_graph()
    r = _validate_shacl(graph, shacl_graph=shape_graph)
    conforms, results_graph, results_text = r

    if not conforms:
        file = open("validation_results.txt", "w", encoding="utf-8")
        file.write(results_text)
        file.close()
        raise Exception(
            "Graph does not conform to schema. Check validation_results.txt for details"
        )


def get_shape_graph():
    current_directory_path = os.path.dirname(__file__)
    shape_path = os.path.join(
        current_directory_path, "..", "..", "ontology", "dist", "combined_schema.ttl"
    )
    return Graph().parse(shape_path, format="turtle")


def get_taxonomy_graph():
    current_directory_path = os.path.dirname(__file__)
    paths = glob.glob(
        os.path.join(
            current_directory_path, "..", "..", "ontology", "taxonomies", "*.ttl"
        )
    )

    graph = Graph()

    for path in paths:
        graph += Graph().parse(path, format="turtle")

    return graph


def keys_to_camel_case(data: dict) -> dict:
    """Converts the keys of a dictionary to camel case"""
    new_data = {}

    for key, value in data.items():
        new_key = to_camel_case(key)
        new_data[new_key] = value

    return new_data


def to_camel_case(input_str: str):
    pascalcase = re.compile(r"([A-Z][a-z]*)*")
    camelcase = re.compile(r"([a-z]*([A-Z][a-z]*)*)")
    uppercase_oneword = re.compile(r"[A-Z]+")

    if uppercase_oneword.fullmatch(input_str):
        return input_str.lower()
    if pascalcase.fullmatch(input_str):
        return input_str[0].lower() + input_str[1:]
    if camelcase.fullmatch(input_str):
        return input_str

    # Handle spaced
    words = input_str.split() if " " in input_str else [input_str]

    pattern = r"[/_.\s-]+"
    words = re.split(pattern, input_str)

    # Ensure the first letter of the first word starts with a lowercase letter
    camel_case_str = words[0].lower()

    # Capitalize the first letter of each subsequent word
    camel_case_str += "".join(word.capitalize() for word in words[1:])

    return camel_case_str
