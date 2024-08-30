import os
from typing import List, Tuple

import openai
import pandas as pd
from dotenv import load_dotenv
from openai.resources.embeddings import CreateEmbeddingResponse

from matching.embed.embedder import Embedder
from matching.utils.serialise import serialise_entity

load_dotenv()


class OpenAIEmbedder(Embedder):
    def __init__(
        self,
        use_cache=True,
        cache_path="data/openai_embeddings_small.json",
        collection_name: str = "openai_small",
        embedding_size=1536,
    ):
        super().__init__(
            use_cache=use_cache,
            cache_path=cache_path,
            collection_name=collection_name,
            embedding_size=embedding_size,
        )

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client: openai.OpenAI = openai.OpenAI(api_key=self.api_key)
        self.latent_size = embedding_size
        self.model = "text-embedding-3-small"

    def calculate_embeddings(self, entity: pd.Series):
        """
        Calculates the embeddings of the entity.
        """

        if "uri" in entity:
            entity = entity.drop("uri")

        serialised = serialise_entity(entity)

        response: CreateEmbeddingResponse = self.openai_client.embeddings.create(
            model=self.model, input=serialised, encoding_format="float"
        )

        self.tokens_used += int(response.usage.total_tokens)

        return response.data[0].embedding

    def embed_serialised(self, serialised: str, uri: str = None):
        """
        Calculates the embeddings of the entity.
        """

        if uri:
            if self.client:
                embeddings = self.client.get(
                    collection_name=self.collection_name, ids=uri
                )
                if len(embeddings) > 0:
                    return embeddings[0]["vector"]

        response: CreateEmbeddingResponse = self.openai_client.embeddings.create(
            model=self.model, input=serialised, encoding_format="float"
        )

        self.tokens_used += int(response.usage.total_tokens)

        return response.data[0].embedding

    def calculate_batch_embeddings(self, entities: List[Tuple[str, pd.Series]]):
        """
        Calculates the embeddings of the entity.
        """

        present = self.client.get(
            collection_name=self.collection_name,
            ids=[entity[0] for entity in entities],
        )

        if len(present) == len(entities):
            print("All entities are already present in the database.")
            return

        for _, elem in enumerate(present):
            idx_to_remove = None
            for idx, entity in enumerate(entities):
                if entity[0] == elem["id"]:
                    idx_to_remove = idx
                    break

            if idx_to_remove is not None:
                entities.pop(idx_to_remove)
                print(
                    f"Removed {elem['id']} from entities to serialise, as it is already present in the database."
                )

        cleaned = [entity[1] for entity in entities]
        cleaned = [entity.drop("uri") for entity in cleaned if "uri" in entity]

        serialised = [serialise_entity(entity) for entity in cleaned]

        response: CreateEmbeddingResponse = self.openai_client.embeddings.create(
            model=self.model, input=serialised, encoding_format="float"
        )

        self.tokens_used += int(response.usage.total_tokens)

        embeddings = []

        for i in range(len(entities)):
            embeddings.append((entities[i][0], response.data[i].embedding))

        self.client.insert(
            collection_name=self.collection_name,
            data=[{"id": uri, "vector": embeddings} for uri, embeddings in embeddings],
        )

        return embeddings
