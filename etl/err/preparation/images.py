import urllib.parse


def generate_image_url(image_type: str, file_name: str):
    '''this function generates the image url for the err images'''

    # this mapping is derived from the ImageType.csv file
    image_type_url_mapping = {
        "1": "https://errproject.org/media/images/err/",  # NARA
        "2": "https://errproject.org/media/images/err/koblenz/800px/",  # Bundesarchiv
        "3": "https://errproject.org/media/images/err/",  # Zi, Münche
    }
    url_start = image_type_url_mapping[image_type]

    file_name = file_name.removeprefix("/")
    file_name = file_name.removeprefix("koblenz/800px/")

    url = url_start + file_name
    url = urllib.parse.quote(url, safe="/:")

    return url
