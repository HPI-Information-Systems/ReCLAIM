"""
Contains classes for generating the neighbourhood of entities.
"""

import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

import pandas as pd
from pymilvus import MilvusClient


class Neighbourhood:
    def __init__(
        self,
        data: pd.DataFrame,
        collection_name: str,
        num_neighbours: int = 50,
    ) -> None:

        super().__init__()
        self.num_neighbours = num_neighbours

        self.similarities_db = MilvusClient(
            os.getenv("MILVUS_DB"),
        )

        self.data = data

        if collection_name not in self.similarities_db.list_collections():
            raise ValueError(f"Collection {collection_name} does not exist.")

        self.collection_name = collection_name

    def find_neighbourhood(self, entity: pd.Series) -> pd.DataFrame:
        """
        Find the neighbourhood of the entity.
        """
        try:
            entity_vector = self.similarities_db.get(
                collection_name=self.collection_name,
                ids=entity["uri"],
            )

            if len(entity_vector) == 0:
                return pd.DataFrame()

            entity_vector = entity_vector[0]["vector"]

            distances = self.similarities_db.search(
                collection_name=self.collection_name,
                data=[entity_vector],
                filter='id != "' + entity["uri"] + '"',
                limit=self.num_neighbours,
            )

            indices = [d["id"] for d in distances[0]]

            return self.data[self.data["uri"].isin(indices)]

        except KeyError:
            return pd.DataFrame()
        except IndexError:
            return pd.DataFrame()
