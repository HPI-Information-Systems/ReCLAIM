import sys
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from munich_goering.crawler import Crawler
from munich_goering.datapoint import Datapoint


class MunichCrawler(Crawler):
    def __init__(self, limit: int = 600000, start: int = 1, wait: int = 50) -> None:
        url = "https://www.dhm.de/datenbank/ccp/dhm_ccp.php"
        super().__init__(
            name="Munich",
            limit=limit,
            start=start,
            wait=wait,
            url=url,
            datapoint_type=MunichDatapoint,
            file_name="munich",
        )

    @staticmethod
    def get_elements_in_page(html_as_soup: BeautifulSoup) -> List[BeautifulSoup]:
        element_starts = html_as_soup.find_all(
            "hr", {"style": "border-bottom:1px solid #666"}
        )
        elements = []

        for start in element_starts:
            element = start
            content = []
            while (element := element.find_next_sibling()) is not None:
                if (
                    element.find(
                        "input", {"type": "button", "value": "Merken", "alt": "Merken"}
                    )
                    is not None
                ):
                    break
                content.append(element)
            elements.append(
                BeautifulSoup("".join([str(x) for x in content]), "html.parser")
            )

        return elements

    @staticmethod
    def get_munich_number(html_as_soup: BeautifulSoup) -> str:
        flashcard_table = html_as_soup.find("table", {"class": "karteikarte"})
        return flashcard_table.find("tr").find("td", {"class": "value"}).text

    @staticmethod
    def get_number_of_results(html_as_soup: BeautifulSoup) -> int:
        """
        Get the number of results from the html.
        :param html_as_soup: The html as a soup object
        :return: The number of results
        """
        div = html_as_soup.find("div", {"class": "resultheader"})
        if div is None:
            return 0
        number_of_results = (
            div.find("h2", {"class": "results"}).text.split(":")[1].strip()
        )

        return int(number_of_results)

    def parse_element(self, element: BeautifulSoup) -> None:
        number = self.get_munich_number(element)
        if "/" in number:
            suffix = "".join([x for x in number.split("/")[1] if x.isdigit()])

            if "[" in suffix:
                suffix = suffix.split("[", maxsplit=1)[0]
            if "-" in suffix:
                suffix = suffix.split("-")

                # check if either suffix is not a number
                if not suffix[0].isnumeric() or not suffix[1].isnumeric():
                    # drop the non-numeric parts
                    suffix = [
                        "".join([x for x in suffix[0] if x.isdigit()]),
                        "".join([x for x in suffix[1] if x.isdigit()]),
                    ]

                for i in range(int(suffix[0]), int(suffix[1]) + 1):
                    datapoint = self.get_or_create_datapoint(
                        f"{number.split('/')[0]}/{i}", raw_number=number
                    )
                    datapoint.parse_html_to_serialisable(element)

            else:
                datapoint = self.get_or_create_datapoint(number, number)
                datapoint.parse_html_to_serialisable(element)
        else:
            datapoint = self.get_or_create_datapoint(number, number)
            datapoint.parse_html_to_serialisable(element)

    def load_all_elements_for_munich_id(self, munich_id: str) -> List[BeautifulSoup]:
        self.browser.get(f"{self.url}?seite=6&fld_1={munich_id}")
        soup = BeautifulSoup(self.browser.page_source, "html.parser").find(
            "div", {"id": "col3_content"}
        )
        number_of_results = self.get_number_of_results(soup)

        print(
            "Loading all elements for munich id",
            munich_id,
            "with",
            number_of_results,
            "results.",
        )

        elements = self.get_elements_in_page(soup)

        if number_of_results <= 20:
            return elements

        cookies = {"PHPSESSID": self.browser.get_cookie("PHPSESSID")["value"]}

        for i in range(1, number_of_results // 20 + 1):
            self.browser.add_cookie(
                {
                    "name": "PHPSESSID",
                    "value": cookies["PHPSESSID"],
                }
            )
            self.browser.get(f"{self.url}?seite=8&current={i*20}")
            soup = BeautifulSoup(self.browser.page_source, "html.parser").find(
                "div", {"id": "col3_content"}
            )
            elements.extend(self.get_elements_in_page(soup))

        return elements

    def crawl(self):
        while self.current <= self.limit + self.start:
            try:
                elements = self.load_all_elements_for_munich_id(str(self.current))

                for element in elements:
                    # parse element
                    self.parse_element(element)

                self.browser.implicitly_wait(self.wait)

                self.current += 1

                # save the data
                self.save()
            except Exception as e:
                print(
                    f"[ERROR] Error while processing {self.current}: {e}",
                    file=sys.stderr,
                )
                self.current += 1
                continue


class MunichDatapoint(Datapoint):
    """
    Class representing a single datapoint in the Munich dataset.
    A datapoint in this case is everything that has been subsumed under a single munich ID.
    (This means that 18/4 and 18/3 are **not** part of the same datapoint class!)
    """

    def __init__(self, munich_id: str, raw_number: str = None, **kwargs):
        super().__init__(id=f"{munich_id}", raw_number=raw_number, **kwargs)

    # def to_dict(self):
    #     return {"munich_id": self.id, **self.data, "raw_number": self.raw_number}

    @staticmethod
    def get_image_links_for_element(element: BeautifulSoup) -> List[str]:
        images = element.find_all("img")
        image_links = []
        if len(images) > 0:
            for img in images:
                image_links.append(f"https://www.dhm.de/datenbank/ccp/{img['src']}")
        return image_links

    def parse_object_photography(self, html_as_soup: BeautifulSoup) -> None:
        # get the img tag
        images = html_as_soup.find_all("img")
        image_links = []
        if len(images) > 0:
            for img in images:
                image_links.append(f"https://www.dhm.de/datenbank/ccp/{img['src']}")

        self.add_data("photographs", image_links)

    def parse_control_number_card(self, html_as_soup: BeautifulSoup) -> None:
        table = html_as_soup.find("table", {"class": "karteikarte"})
        rows = table.find_all("tr")
        data = {}

        for row in rows:
            key = row.find("td").text.split(":")[0].strip()
            value = row.find("td", {"class": "value"}).text
            data[key] = value

        data["images_of_card"] = self.get_image_links_for_element(html_as_soup)

        self.add_data("control_number_card", data)

    def parse_restitution_card(self, html_as_soup: BeautifulSoup) -> None:
        table = html_as_soup.find("table", {"class": "karteikarte"})
        rows = table.find_all("tr")
        data = {}

        for row in rows:
            key = row.find("td").text.split(":")[0].strip()
            value = row.find("td", {"class": "value"}).text

            match key:
                case "Münchener Nr.":
                    continue
                case "Datierung (Objekt)":
                    key = "object_date"
                case "Datierung":
                    date_format = "%Y.%m.%d"
                    if "Eingang/Receipt" in value:
                        key = "receipt_date"
                    elif "Ausgang/Issue" in value:
                        key = "dispatch_date"
                    value = str(
                        datetime.strptime(
                            value.split(" ")[0].strip(), date_format
                        ).strftime("%d.%m.%Y")
                    )
                case "Material/Technik":
                    key = "material"
                case "Kartei":
                    continue

            if key in data:
                if isinstance(data[key], list):
                    data[key] = [value, *data[key]]
                else:
                    data[key] = [value, data[key]]
            else:
                data[key] = value
        self.add_data_from_dict(data)

        self.add_data(
            "restitution_card_images", self.get_image_links_for_element(html_as_soup)
        )

    def parse_unknown_card(self, html_as_soup: BeautifulSoup, title: str) -> None:
        table = html_as_soup.find("table", {"class": "karteikarte"})
        rows = table.find_all("tr")
        data = {}

        for row in rows:
            key = row.find("td").text.split(":")[0].strip()
            value = row.find("td", {"class": "value"}).text

            if key in data:
                if isinstance(data[key], list):
                    data[key] = [value, *data[key]]
                else:
                    data[key] = [value, data[key]]
            else:
                data[key] = value

        data["images_of_element"] = self.get_image_links_for_element(html_as_soup)

        self.add_data(title, data)

    def parse_html_to_serialisable(self, html_as_soup: BeautifulSoup) -> None:
        # get the type of card
        card_type = html_as_soup.find("h2")
        card_type_elements = card_type.text.split("-")
        match card_type_elements[-1].strip():
            case "Objektfotografien":
                self.parse_object_photography(html_as_soup)
            case "Kontrollnummernkartei":
                self.parse_control_number_card(html_as_soup)
            case "Restitutionskartei":
                self.parse_restitution_card(html_as_soup)
            case _:
                self.parse_unknown_card(
                    html_as_soup, " ".join(card_type_elements[1:]).strip()
                )
