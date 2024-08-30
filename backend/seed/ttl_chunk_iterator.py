############################################
############################################
#
# Deprecation Notice: Since the memory contraints of neo4j have been lifted, a chunkwise ingestion is not required anymore
#
############################################
############################################

import rdflib


class TTLChunkIterator:
    def __init__(self, data: str, namespaces: str, chunk_size: int):
        self.graph = rdflib.Graph()
        self.graph.parse(data=data, format="ttl")
        self.namespaces = namespaces
        self.chunk_size = chunk_size

    def get_new_graph(self):
        new_graph = rdflib.Graph()
        new_graph.parse(data=self.namespaces, format="ttl")
        return new_graph

    def get_next_chunk(self):
        entity_count = 0
        current_graph = rdflib.Graph()

        for subject, _, _ in self.graph.triples((None, None, None)):
            entity_count += 1
            for _, predicate, object in self.graph.triples((subject, None, None)):
                current_graph.add((subject, predicate, object))

            if entity_count > self.chunk_size:
                yield current_graph.serialize(format="ttl")
                current_graph = self.get_new_graph()
                entity_count = 0

        yield current_graph.serialize(format="ttl")
