from bs4 import BeautifulSoup


class Datapoint:
    def __init__(self, id: str, raw_number: str = None):
        self.id = id
        self.raw_number = raw_number
        self.data = {}

    def __hash__(self):
        return self.id.__hash__()

    def add_data(self, key: str, value: str | dict | list) -> None:
        """
        Add data to the datapoint.
        Can be overriden by subclasses
        :return:
        """
        self.data[key.lower()] = value

    def add_data_from_dict(self, data: dict) -> None:
        """
        Add data to the datapoint.
        Can be overriden by subclasses
        :param data:
        :return:
        """
        for key, value in data.items():
            self.data[key.lower()] = value

    def to_dict(self):
        return {"id": self.id, **self.data, "raw_number": self.raw_number}

    def parse_html_to_serialisable(self, html_as_soup: BeautifulSoup) -> None:
        """
        To be overriden by the subclasses.
        :param html_as_soup:
        :return: None
        """
        pass
