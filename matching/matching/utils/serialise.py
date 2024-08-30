import pandas as pd

from matching.config import Settings


def serialise_entity(data: pd.Series, exclude_uri=False) -> str:
    """
    Serialise the entity.
    """

    if Settings.get_serialisation_format() == "ditto":
        serialised = "[COL] "
        for col in data.index:
            if col == "uri" and exclude_uri:
                continue
            if col not in data.index:
                continue
            if data[col] == "nan":
                continue

            serialised += f"{col} [VAL] {data[col]} [COL] "
        serialised = serialised[:-6]
    elif Settings.get_serialisation_format() == "json":
        serialised = data.to_json()

    return serialised
