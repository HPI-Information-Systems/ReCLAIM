"""
Contains all logic for feature extraction
"""

import pandas as pd


def get_relevant_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df[
        [
            col
            for col in df.columns
            if not "derived" in col.lower()
            and not (col.startswith("consistsOfMaterial") and not col.endswith("uri"))
            and not (col.startswith("classifiedAs") and not col.endswith("uri"))
            and not (col == "collectedIn_uri")
            and not ("image" in col.lower())
            and not (col == "createdBy_uri")
            and not "similar" in col.lower()
        ]
    ].copy()

    if "source" not in df.columns:
        df["source"] = df["uri"].apply(lambda x: x.split("/")[4])

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df
