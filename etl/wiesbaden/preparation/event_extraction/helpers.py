import json
import pandas as pd
import numpy as np
from ast import literal_eval

from common.event_extraction.helpers import measure_vector_distance
from .prepare_arrival_condition import prepare_arrival_condition


def get_embedding_of_free_text_val(
    embeddings: pd.DataFrame, free_text_val: str
) -> list[float]:
    return embeddings[embeddings["history-and-ownership"] == free_text_val][
        "embedding"
    ].values[0]


def append_embeddings_to_dynamic_examples(
    embeddings: pd.DataFrame, dynamic_examples: list[dict]
) -> list[dict]:
    """
    This function is used to include the corresponding embeddings in the labeled examples.
    """

    for example in dynamic_examples:
        embedding = get_embedding_of_free_text_val(
            embeddings=embeddings,
            free_text_val=example["input"]["history_and_ownership"],
        )
        example["hao_embedding"] = embedding

    return dynamic_examples


def select_dynamic_exmaples(
    free_text_value_to_parse: str,
    embeddings_df: pd.DataFrame,
    dynamic_examples: list[dict],
    number_of_examples: int,
) -> str:
    """
    This function is used to select dynamic examples that are most similar to the free_test_value_to_parse.
    """

    if number_of_examples > len(dynamic_examples):
        raise ValueError(
            "Number of examples to retrieve is higher than the number of dynamic examples available."
        )

    # Select the cached embedding to the corresponding free-text value to parse
    free_text_embedding = embeddings_df[
        embeddings_df["history-and-ownership"] == free_text_value_to_parse
    ]["embedding"].values[0]

    # Find top n dynamic examples that are most similar to the value to parse
    free_text_embedding_similarities = np.array(
        list(
            map(
                lambda example: measure_vector_distance(
                    np.array(literal_eval(example["hao_embedding"])),
                    np.array(literal_eval(free_text_embedding)),
                ),
                dynamic_examples,
            )
        )
    )
    most_similar_indices = np.argsort(free_text_embedding_similarities)[
        :number_of_examples
    ]

    # Return the most similar example without the embeddings field
    return [
        {k: v for k, v in dynamic_examples[i].items() if k != "hao_embedding"}
        for i in most_similar_indices
    ]


def generate_labelling_template(representatives: pd.DataFrame, output_fp: str):
    """
    This function is used to convert a CSV file with chosen cluster representatives
    into a JSON template that we can use for manual annotation.
    """

    template_data = []

    for _, row in representatives.iterrows():
        template_data.append(
            {
                "input": {
                    "history_and_ownership": row["history-and-ownership"],
                    "depot_possessor": row["depot-possessor"],
                    "depot_number": row["depot-number"],
                    "arrival_condition": prepare_arrival_condition(
                        row["arrival-condition"], row["condition-and-repair-record"]
                    ),
                    "arrival_date": row["arrival-date"],
                    "exit_date": row["exit-date"],
                },
                "event_chain": [],
            }
        )

    json.dump(template_data, open(output_fp, "w"), indent=4)


def save_result_to_cache(cache: JsonCache, input: dict, result: str):
    """
    Saves
    """

    # parse content as JSON
    try:
        # Sometimes the LLM produces this prefix
        if result.startswith("```json"):
            result = result[7:-3]

        parsed = json.loads(result)
        cache_key = json.dumps(input)

        cache.set(cache_key, parsed["structured"])

    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return e
