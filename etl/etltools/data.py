import os
import io

import pandas as pd
from pandas import DataFrame


def data_path(*, source_id: str, file_path: str) -> str:
    '''returns the path to the data file'''
    current_directory_path = os.path.dirname(__file__)
    return os.path.join(
        current_directory_path, "..", "..", "data", source_id, file_path
    )


def csv_as_dataframe(*, source_id: str, file_path: str, limit: int = None) -> DataFrame:
    '''returns the data from the csv file as a DataFrame'''
    csv_path = data_path(source_id=source_id, file_path=file_path)

    return pd.read_csv(csv_path, dtype=str, nrows=limit)


def csv_as_lines(*, source_id: str, file_path: str, limit: int = None) -> list[dict]:
    '''returns the data from the csv file as a list of dictionaries'''
    dataframe = csv_as_dataframe(source_id=source_id, file_path=file_path, limit=limit)
    return [line.to_dict() for _, line in dataframe.iterrows()]


def write_turtle(graph, output_path: str):
    '''writes the graph to a turtle file'''
    try:
        with io.open(
            output_path, "w", encoding="utf-8", buffering=1024 * 1024 * 10
        ) as file:
            file.write(graph.serialize(format="turtle"))
            file.close()
    except Exception as e:
        print("An error ocurred while writing the turtle file:")
        print(e)
