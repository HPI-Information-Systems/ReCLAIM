import enum
import os
from typing import Any, List, Tuple

import pandas as pd
from pymilvus import MilvusClient

from matching.utils.db.features import get_relevant_features


class SupportedColumns(enum.Enum):
    MATERIAL = "material"
    AUTHOR = "author"
    TITLE = "title"
    CLASSIFICATION = "classification"


class PretrainPairGenerator:
    def __init__(
        self,
        data: pd.DataFrame,
        export_path: str = "pretrain_pairs_all.csv",
        embedding_collection: str = "openai_small",
        positive_threshold: float = 0.95,
        negative_threshold: float = 0.85,
    ):
        self.data: pd.DataFrame = data
        self.pairs: List[Tuple[str, str, int]] = []
        self.export_path = f"data/{export_path}"

        self.client = MilvusClient(
            os.getenv("MILVUS_DB"),
        )

        self.embedding_collection = embedding_collection

        if embedding_collection not in self.client.list_collections():
            raise ValueError("Collection not found in Milvus.")

        self.positive_threshold = positive_threshold
        self.negative_threshold = negative_threshold

    @staticmethod
    def generate_data_subset(
        data: pd.DataFrame, labelled_samples: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        Generate a subset of the data for pre-training.
        :param data: The data to generate the subset from.
        :param export: Whether to export the data to a csv file.
        :param labelled_samples: The labelled samples to exclude from the data. Expected to be a DataFrame of candidate-pairs.
        """

        data = get_relevant_features(data)

        if labelled_samples is not None:
            positive_samples = labelled_samples[labelled_samples["label"] == 1]
            excluded_uris = (
                positive_samples["1_uri"].tolist() + positive_samples["2_uri"].tolist()
            )
            data = data[~data["uri"].isin([excluded_uris])].copy()
            data.reset_index(drop=True, inplace=True)
            print(
                f"Excluded {len(set(excluded_uris))} labelled samples from the data as they are part of a match."
            )

            labelled_columns = labelled_samples.columns.str[2:]

            labelled_columns = labelled_columns.drop_duplicates()

            data = data[[col for col in data.columns if col in labelled_columns]].copy()

        return data

    @staticmethod
    def fix_linz_createdBy_names(db: pd.DataFrame) -> pd.DataFrame:
        for idx, row in db.iterrows():
            if row["collectedIn_name"] == "Linzer Sammlung":
                db.at[
                    idx, "createdBy_name"
                ] = f"{row['createdBy_firstName']} {row['createdBy_lastName']}"

        return db
