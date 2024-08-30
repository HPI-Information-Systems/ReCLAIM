import os
from typing import List

import pandas as pd
from pymilvus import MilvusClient

from matching.utils.serialise import serialise_entity


class Embedder:
    def __init__(
        self,
        use_cache=True,
        cache_path="data/entity_embeddings.json",
        collection_name: str = "openai_small",
        embedding_size=1536,
    ):

        super().__init__()

        self.use_cache = use_cache
        self.export_path = cache_path

        if not os.path.exists(self.export_path):
            self.cache = pd.DataFrame(columns=["embedding"], index=["uri"])
        else:
            self.cache = pd.read_json(self.export_path, orient="index")
        # self.cache.columns = ['embedding']

        self.cache["embedding"] = self.cache["embedding"].astype("object")
        self.tokens_used = 0

        self.client: MilvusClient = MilvusClient(os.getenv("MILVUS_DB"))

        if collection_name not in self.client.list_collections():
            self.client.create_collection(
                collection_name=collection_name,
                dimension=embedding_size,
                id_type="string",
                max_length=1024,
            )

        self.collection_name = collection_name

    def exists_in_database(self, uri: str):
        """
        Checks if the entity is in the database.
        """

        if not self.client:
            return False

        if entity := self.client.get(collection_name=self.collection_name, ids=uri):
            if len(entity) > 0:
                print(f"Found {uri} in the database")
                return True

        return False

    def calculate_embeddings(self, entity: pd.DataFrame):
        """
        Calculates the embeddings of the entity.
        """
        raise NotImplementedError

    def calculate_batch_embeddings(self, entities: List[pd.Series]):
        raise NotImplementedError

    def embed(self, entity: pd.DataFrame):
        """
        Embeds the entity and stores the embeddings in a json cache.
        """
        uri = entity["uri"]

        if self.exists_in_database(uri):
            entity = self.client.get(
                collection_name=self.milvus_collection_name, ids=uri
            )

            return entity[0]["vector"]

        embeddings = self.calculate_embeddings(entity)

        self.client.insert(
            collection_name=self.collection_name,
            data=[{"id": uri, "vector": embeddings}],
        )

        return embeddings

    def batch_embed(self, entities: pd.DataFrame):
        """
        Embeds a batch of entities and stores the embeddings in a json cache. We assume that the entities have a uri column.
        """

        batch: List[int, pd.Series] = []
        batch_size = 0

        for idx, entity in entities.iterrows():
            if idx % 100 == 0:
                print(f"At index {idx}")

            naive_serialisation_length = len(serialise_entity(entity))
            uri = entity["uri"]

            if batch_size + naive_serialisation_length > 8191:
                # We have to send the batch
                self.calculate_batch_embeddings(batch)

                batch = []
                batch_size = 0

            batch.append((uri, entity))
            batch_size += naive_serialisation_length

            if self.tokens_used > 50000000:
                print(f"Used {self.tokens_used} tokens, stopping")
                break

        print(f"Used {self.tokens_used} token(s) in total")
