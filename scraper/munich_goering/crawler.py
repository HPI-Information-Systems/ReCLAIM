import json
import os
from datetime import datetime
from typing import List

from selenium import webdriver

from .datapoint import Datapoint


class Crawler:
    """
    Base class for the webcrawler for the DHM datasets.
    :param limit: The maximum number of pages to crawl
    :param start: The page to start crawling from
    :param wait: The time (in ms) to wait between requests
    """

    def __init__(
        self,
        url: str,
        name: str,
        limit: int = 100,
        start: int = 0,
        wait: int = 100,
        datapoint_type=Datapoint,
        file_name: str = None,
    ) -> None:
        self.limit = limit
        self.datapoint_type = datapoint_type
        self.crawled_data: List[datapoint_type] = []
        self.start = start
        self.current = start
        self.wait = wait
        self.url = url
        self.name = name
        self.file_name = f"{file_name}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.browser = webdriver.Chrome(options=options)

    def __del__(self):
        self.browser.close()
        self.browser.quit()

    def crawl(self):
        """
        The main crawling function. This function should be overwritten by subclasses.
        """
        pass

    def get_or_create_datapoint(
        self, datapoint_id: str, raw_number: str = None
    ) -> Datapoint:
        """
        Get or create a datapoint.
        :param datapoint_id: The id (hash) of the datapoint
        """

        if raw_number is None:
            raw_number = datapoint_id

        datapoint = self.datapoint_type(datapoint_id, raw_number=raw_number)

        for point in self.crawled_data:
            if point.id == datapoint_id:
                return point

        self.crawled_data.append(datapoint)

        return datapoint

    def save(self) -> None:
        """
        Save the data to a file.
        """

        if not os.path.exists("./data"):
            os.mkdir("./data")

        serialized_datapoints = [datapoint.to_dict() for datapoint in self.crawled_data]

        with open(f"./data/{self.file_name}.json", "a", encoding="utf-8") as file:
            json.dump(serialized_datapoints, file, indent=2, ensure_ascii=False)

        self.crawled_data = []
