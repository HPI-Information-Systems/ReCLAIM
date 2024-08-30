import json
import pandas as pd
import numpy as np


def load_data_source(
    data_source_file_path: str, relevant_columns: list[str]
) -> pd.DataFrame:
    """
    This function loads and prepares a csv data source. It removes all NaN values and drops duplicate values.

    :param data_source_file_path: Path of the csv source file
    :param relevant_columns: List of names of columns that should be considered in the event extraction.
    """

    df = pd.read_csv(data_source_file_path, dtype=str, keep_default_na=False)[
        relevant_columns
    ]
    df = df.map(
        lambda x: None if x == "" or x.lower() == "nan" else x
    )  # remove "nan" strings from df
    df.drop_duplicates(relevant_columns, keep=False, inplace=True)

    return df


def measure_vector_distance(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    return np.linalg.norm(vector_a - vector_b)
