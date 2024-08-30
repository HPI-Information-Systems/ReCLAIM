import os
import pandas as pd
from etl import etltools


def upload_files():
    """this function is for uploading the pictures of the property cards to azure blob storage
    also it creates a csv to map filenames to remote urls"""

    picture_directory = "../../../data/marburg/Foto_Marburg"

    file_names = os.listdir(picture_directory)
    image_df = pd.read_csv("imagefilenames_to_url.csv")
    image_dict = dict(zip(image_df["filename"], image_df[" url"]))
    count_yes = 0
    count_no = 0

    for filename in file_names:
        # to distinguish between the marburg fotos and the
        filename_short = filename.split(".")[0]

        if filename_short not in image_dict.keys():
            remote_url = etltools.image.upload_file(
                directory_name="marburg",
                file_path=os.path.join(picture_directory, filename),
            )
            if remote_url is not None:
                with open("imagefilenames_to_url.csv", "a") as file:
                    file.write(f"\n{filename_short},{remote_url}")
                    print(f"{filename} uploaded to {remote_url}")
            count_no += 1
        else:
            count_yes += 1

    print(f"Already uploaded: {count_yes}")
    print(f"Not uploaded: {count_no}")


if __name__ == "__main__":
    upload_files()
