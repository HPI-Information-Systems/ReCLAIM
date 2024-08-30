import pandas as pd
from datetime import datetime


def save_to_file(file_type, data, filename: str) -> None:
    df = pd.DataFrame(data)
    try:
        match file_type:
            case "json":
                df.to_json(
                    f'{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_{filename}.json',
                    force_ascii=False,
                    indent=4,
                    orient="records",
                )
            case "csv":
                df.to_csv(
                    f'{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}_{filename}.csv'
                )
            case _:
                print("Unknown file type")
    except:
        print("Error saving file")
        print(df.head())
