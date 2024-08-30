from etl import etltools
import re
import requests
from bs4 import BeautifulSoup
import os

data = etltools.data.csv_as_lines(
    source_id="marburg",
    file_path="29-4-24-marburg-export.csv",
)
picture_directory = "../../../data/marburg/Foto_Marburg/"

# regex matches image numbers with multiple digits (193456), that can be separated by a space (193 456), a slash (193/456).
# also the numbers can start with L or A (LA193456,A193 456, LA 193/456)
regex = r"L?A?\s?\d+\/?\s?\d+"

counter = 0
many_results = 0
exist = 0
nan = 0
nomatch = 0
notmatches = []
noResults = 0

for row in data:
    if str(row["image-number"]) == "nan":
        nan += 1
        continue

    regex_match = re.search(regex, row["image-number"])
    if regex_match is None:
        nomatch += 1
        notmatches.append(row["image-number"])
        continue

    image_number = regex_match.group(0)
    image_number = image_number.strip()

    # if there is a space in the image number, we will remove it (only for short numbers to avoid joining two numbers)
    if len(image_number) < 9:
        image_number = image_number.replace(" ", "")

    # sometimes there are 2 image numbers, we will only take the first one (only occures about 10 times)
    if re.search(r"\d \d", image_number):
        image_number = image_number.split(" ")[0]

    # if the image number is 6 digits, we will add a dot in the middle (othervise the search will not work)
    if re.match(r"\d{6}", image_number):
        image_number_prepared = image_number[0:3] + "." + image_number[3:6]
    # othervise we will add quotes around the number to match exactly and decrease the number of results
    else:
        image_number_prepared = '"' + image_number + '"'

    identifier = row["filename-front"]
    filename = identifier + ".jpg"
    print(identifier + image_number_prepared)

    # check if the picture is already downloaded
    if os.path.isfile(picture_directory + filename):
        print("File already exists: " + filename)
        exist += 1
        continue

    url = (
        "https://www.bildindex.de/ete?action=queryupdate&desc="
        + image_number_prepared
        + "&index=pic-all"
    )

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("img", class_="thumb lazy")

    # handle multiple results
    if len(results) > 1:
        print(str(image_number) + " has more than one result: ", len(results))
        many_results += 1
        continue

    # handle no results
    if len(results) == 0:
        print("No results found")
        noResults += 1
        notmatches.append(row["image-number"])
        continue

    for result in results:
        print(str(counter))

        image_url = result["edp-src"]

        # there is one broken image on the website, so we will skip it
        if image_url == "/images/nopic_large.png":
            print("No image found")
            continue

        image = requests.get(image_url)

        with open(picture_directory + filename, "wb") as f:
            f.write(image.content)
            counter += 1


print("Many results: ", many_results)
print("Exist: ", exist)
print("Saved: ", counter)
print("Nan: ", nan)
print("Nomatch: ", nomatch)
print("No results: ", noResults)
