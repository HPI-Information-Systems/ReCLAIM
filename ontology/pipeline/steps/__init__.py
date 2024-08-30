from rdflib import Graph
from . import infer_shapes


def run_all(graph: Graph):
    infer_shapes.run(graph)
