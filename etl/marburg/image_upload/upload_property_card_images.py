import os
import pandas as pd
from etl import etltools


def upload_files():
    """this function is for uploading the pictures of the property cards to azure blob storage
    also it creates a csv to map filenames to remote urls"""

    picture_directory = "../../data/marburg/Bundesarchiv_marburg_property_cards"

    file_names = os.listdir(picture_directory)

    image_df = pd.read_csv("imagefilenames_to_url.csv")
    image_dict = dict(zip(image_df["filename"], image_df[" url"]))
    count_yes = 0
    count_no = 0

    for filename in file_names:
        if filename not in image_dict.keys():
            remote_url = etltools.image.upload_file(
                directory_name="marburg",
                file_path=os.path.join(picture_directory, filename),
            )
            if remote_url is not None:
                with open("imagefilenames_to_url.csv", "a") as file:
                    file.write(f"\n{filename},{remote_url}")
                    print(f"{filename} uploaded to {remote_url}")
            count_no += 1
        else:
            count_yes += 1

    print(f"Already uploaded: {count_yes}")
    print(f"Not uploaded: {count_no}")


if __name__ == "__main__":
    upload_files()
