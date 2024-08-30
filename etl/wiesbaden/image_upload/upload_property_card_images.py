import os

from etltools.image import upload_file


def upload_files():
    """this function is for uploading the pictures of the property cards to azure blob storage
    also it creates a csv to map filenames to remote urls"""

    picture_directory = "../../data/wccp/Bundesarchiv_wccp_property_cards"

    for filename in os.listdir(picture_directory):
        remote_url = upload_file(
            directory_name="wccp", file_path=os.path.join(picture_directory, filename)
        )
        if remote_url is not None:
            with open("imagefilenames_to_url.csv", "a") as file:
                file.write(f"\n{filename},{remote_url}")
                print(f"{filename} uploaded to {remote_url}")


if __name__ == "__main__":
    upload_files()
