import mimetypes
import os
import random
import string
import uuid
from dotenv import load_dotenv

import requests
from azure.storage.blob import BlobServiceClient, ContentSettings

load_dotenv("../.env")


def generate_random_slug(length: int = 4) -> str:
    """
    Generates a random slug of a given length.
    :param length: The length of the slug to generate.
    :return: The generated slug.
    """
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    ).lower()


def upload_file(
    directory_name: str,
    file_path: str,
    file_name: str = None,
    file_extension: str = None,
):
    """
    Uploads a file to Azure Blob Storage and returns a persistent URL of it.
    """

    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        )

    except Exception as e:
        print(e)

        return None

    if not file_name:
        file_name = os.path.basename(file_path)

    if not file_extension:
        file_extension = os.path.splitext(file_name)[1][1:]

    file_name_without_extension = file_name.replace(".jpg", "").replace(".png", "")

    file_name = f"{directory_name}/{file_name_without_extension}"

    container_client = blob_service_client.get_container_client("images")
    if not container_client.exists():
        container_client.create_container()

    unslugged_file_name = file_name

    while container_client.get_blob_client(f"{file_name}.{file_extension}").exists():
        file_name = f"{unslugged_file_name}_{generate_random_slug(5)}"

    file_name = f"{file_name}.{file_extension}"

    with open(file_path, "rb") as data:
        blob_client = container_client.upload_blob(
            name=file_name,
            data=data,
            content_settings=ContentSettings(
                content_type=mimetypes.guess_extension(file_name)
                or "application/octet-stream"
            ),
        )

    sanitised_url = blob_client.url.split("?")[0]

    return sanitised_url


def get_image_type(file_path: str):
    """
    Returns the type of an image file.
    :param file_path: The path of the image file.
    :return: The type of the image file, either JPEG or PNG.
    """

    with open(file_path, "rb") as f:
        if f.read(2) == b"\xff\xd8":
            return "jpg"
        elif f.read(8) == b"\x89PNG\r\n\x1a\n":
            return "png"
        else:
            raise ValueError("Unsupported image type.")


def blob_storage_endpoint():
    """
    Returns the endpoint of the Azure Blob Storage.
    """
    return os.getenv("AZURE_STORAGE_CONNECTION_STRING").split(";")[0].split("=")[1]


def is_already_hosted(file_url: str) -> bool:
    """
    Returns, if the image for a given url is already being hosted by us.
    """
    if file_url.startswith(blob_storage_endpoint()):
        return True

    return False


def upload_from_url(
    image_url: str, identifier: str, source_name: str = "unkown"
) -> str:
    """
    Uploads an externally hosted image to Azure Blob Storage and returns a persistent URL of it.
    """
    if is_already_hosted(image_url):
        return image_url

    with requests.get(image_url, stream=True) as r:
        r.raise_for_status()

        with open(tmp_name := f"temp_image_upload_{uuid.uuid4()}", "wb") as f:
            try:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

                file_type = get_image_type(tmp_name)
                image_url = upload_file(source_name, tmp_name, identifier, file_type)
            except Exception as e:
                raise e
            finally:
                os.remove(tmp_name)

    return image_url
