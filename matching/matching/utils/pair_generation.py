"""
Functions to generate the matchable pairs from the data.
"""
import pandas as pd


def naive_pair_generation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate matchable pairs from the data.
    """

    paired_data = pd.DataFrame()

    for i in range(len(data)):
        right = data.iloc[i]
        right = right.add_prefix("1_")
        for j in range(i + 1, len(data)):
            left = data.iloc[j]
            left = left.add_prefix("2_")

            pair = pd.DataFrame(
                {
                    **right.to_dict(),
                    **left.to_dict(),
                    "label": 1,
                },
                index=[0],
            )

            paired_data = pd.concat([paired_data, pair], ignore_index=True)

            print(f"Total pairs: {len(paired_data)}", end="\r")

    return paired_data
