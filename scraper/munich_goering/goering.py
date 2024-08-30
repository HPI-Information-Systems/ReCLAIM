import re

import requests
from bs4 import BeautifulSoup

import munich_goering.utils as utils
from .crawler import Crawler
from .datapoint import Datapoint


def goering_alpha():
    goering_link = "https://www.dhm.de/datenbank/goering/dhm_goering.php?seite=5&"

    def get_goering_str_id(goering_id: int | str):
        current_id_str = str(goering_id).zfill(5)
        return f"RMG{current_id_str}"

    def get_rmd_addendum(goering_id: str | int) -> str:
        return f"fld_0={get_goering_str_id(goering_id)}"

    def goering_finished(html: BeautifulSoup, goering_id: str) -> bool:
        return (
            html.find(
                string=re.compile("Es gibt keinen Datensatz mit der laufenden Nummer.*")
            )
            is not None
        )

    def parse_goering_page(html: BeautifulSoup, goering_id: int):
        main_div = html.find("div", {"id": "main"})
        parseable_content = main_div.find("div", {"id": "col3_content"})

        try:
            other = {}
            title = parseable_content.find("h2")
            painter_h3 = parseable_content.find("h3")

            if painter_h3:
                type_of_painting = painter_h3.find_next_sibling("p")
            else:
                type_of_painting = None

            mue_nr = parseable_content.find(string=re.compile("Mü-Nr.:.*"))
            if mue_nr:
                mue_nr = mue_nr.split(":")[1].strip()

            mue_link = parseable_content.find(
                "a", string=re.compile("Informationen MCCP-Datenbank")
            )

            other_signatures = parseable_content.find(
                string=re.compile("Sonstige Signatur:.*")
            )
            if other_signatures:
                other["signatures"] = "".join(other_signatures.split(":")[1:])

            rm_nr = parseable_content.find(string=re.compile("RM-Nr.:.*"))
            if rm_nr:
                rm_nr = rm_nr.split(":")[1].strip()

            previous_owner_h3 = parseable_content.find(
                "h3", string=lambda text: "Vorbesitz" in text
            )

            if previous_owner_h3:
                previous_owner = previous_owner_h3.find_next_sibling("p")
            else:
                previous_owner = None

            try:
                delivery = parseable_content.find(
                    "h3", string=lambda text: "Einlieferung" in text
                ).find_next_sibling("p")
            except:
                delivery = None

            try:
                after_1945 = parseable_content.find(
                    "h3", string=lambda text: "Verbleib nach 1945" in text
                ).find_next_sibling("p")
            except:
                after_1945 = None

            link_to_painting = parseable_content.find("div", {"style": ""}).find("a")

            data = {
                "id": get_goering_str_id(id),
                "title": title.text if title else None,
                "painter": painter_h3.text if painter_h3 else None,
                "mue_nr": mue_nr,
                "mue_link": f"https://www.dhm.de{mue_link['href']}"
                if mue_link
                else None,
                "rm_nr": rm_nr,
                "previous_owner": previous_owner.text if previous_owner else None,
                "delivery": delivery.text if delivery else None,
                "after_1945": after_1945.text if after_1945 else None,
                "type_of_painting": type_of_painting.text if type_of_painting else None,
                "link_to_painting": link_to_painting["href"]
                if link_to_painting
                else None,
                "other": {**other},
            }

            return data

        except Exception as e:
            print(e)
            print("Error parsing page: " + str(id))
            return

    def get_soup(current_id: int):
        content = requests.get(
            goering_link + "&" + get_rmd_addendum(current_id)
        ).content
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def scrape_goering_collection():
        current_id = 1

        print("Scraping the Goering collection")

        data = []

        while not goering_finished((soup := get_soup(current_id)), current_id):
            print(
                "Scraping url: "
                + goering_link
                + "&"
                + get_rmd_addendum(current_id)
                + " with id: "
                + str(current_id)
            )

            data.append(parse_goering_page(soup, current_id))

            current_id += 1

        utils.save_to_file("json", data, "goering_collection")

        print("✅ Finished scraping the Goering collection")

    scrape_goering_collection()


class GoeringCrawler(Crawler):
    def __init__(self, limit: int = 200, start: int = 1, wait: int = 50) -> None:
        url = "https://www.dhm.de/datenbank/goering/dhm_goering.php"
        super().__init__(
            name="Munich",
            limit=limit,
            start=start,
            wait=wait,
            url=url,
            datapoint_type=GoeringDatapoint,
        )


class GoeringDatapoint(Datapoint):
    pass
