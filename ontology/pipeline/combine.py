import glob
import os

from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax

from .error import BuildError


def get_subgraph_from_file(source_file_path: str) -> Graph:
    graph = Graph()

    try:
        graph.parse(source_file_path, format="ttl")
    except BadSyntax as e:
        raise BuildError("Syntax error in file: " + source_file_path, str(e))

    return graph


def get_source_file_paths() -> list[str]:
    current_directory_path = os.path.dirname(__file__)
    return glob.glob(os.path.join(current_directory_path, "..", "src", "**/*.ttl")) + glob.glob(
        os.path.join(current_directory_path, "..", "src", "*.ttl"))


def get_combined_graph() -> Graph:
    combined_graph = Graph()
    combined_graph.bind("jdcrp", "https://graph.jdcrp.org/schema#")

    for file_path in get_source_file_paths():
        combined_graph += get_subgraph_from_file(file_path)

    return combined_graph
