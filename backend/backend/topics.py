from typing import Dict, List


class Topic:
    """
    Represents a topic for the advanced search. A topic can be selected in the advanced search, to search for attributes across different entity types with one search topic.
    Includes a tooltip for the frontend and the attributes that are searched internally.
    The attributes are a dictionary with the entity type as key and the list of all attributes within that entity type to be searched as value.
    """

    def __init__(self, tooltip: str, searched_attributes: Dict[str, List[str]]) -> None:
        self.tooltip = tooltip
        self.searched_attributes = searched_attributes


def get_cultural_asset_topics() -> Dict[str, Topic]:
    return {
        "Title": Topic(
            "Title of the cultural asset", {"CulturalAsset": ["jdcrp__title"]}
        ),
        "Physical Appearance": Topic(
            "Physical appearance of the cultural asset, including material, classification, weight, and measurements",
            {
                "CulturalAsset": [
                    "jdcrp__physicalDescription",
                    "jdcrp__physicalConditionDescription",
                    "jdcrp__identifyingMarks",
                    "jdcrp__annotation",
                    "jdcrp__weight",
                    "jdcrp__measurements",
                ],
                "Material": ["jdcrp__name"],
                "Classification": ["jdcrp__name"],
            },
        ),
        "Material": Topic(
            "Structured information about the material the cultural asset is made of",
            {"Material": ["jdcrp__name"]},
        ),
        "Classification": Topic(
            "Structured information about the cultural asset's classification",
            {"Classification": ["jdcrp__name"]},
        ),
        "Archival Information": Topic(
            "Information from the archival source of the cultural asset and bibliography",
            {
                "CulturalAsset": [
                    "jdcrp__archivalSourceDescription",
                    "jdcrp__bibliography",
                ],
                "Person": ["jdcrp__archivalSourceDescription"],
            },
        ),
        "History and Provenance": Topic(
            "Descriptions of the history of the cultural asset and related persons",
            {
                "CulturalAsset": [
                    "jdcrp__creationDate",
                    "jdcrp__provenanceDescription",
                    "jdcrp__preConfiscationHistoryDescription",
                    "jdcrp__postConfiscationHistoryDescription",
                    "jdcrp__currentRemainDescription",
                ],
                "Person": ["jdcrp__historyDescription"],
            },
        ),
        "Collection": Topic(
            "Information about the collection the cultural asset is part of",
            {
                "Collection": [
                    "jdcrp__name",
                    "jdcrp__abbreviation",
                    "jdcrp__description",
                ]
            },
        ),
        "Location": Topic(
            "Locations of the cultural asset and related persons",
            {
                "Location": [
                    "jdcrp__description",
                    "jdcrp__street",
                    "jdcrp__city",
                    "jdcrp__region",
                    "jdcrp__country",
                ]
            },
        ),
        "Person Names": Topic(
            "Persons related to the cultural asset",
            {
                "Person": [
                    "jdcrp__firstName",
                    "jdcrp__lastName",
                    "jdcrp__name",
                    "jdcrp__pseudonym",
                ]
            },
        ),
        "Birth Dates": Topic(
            "Birth dates of persons related to the cultural asset",
            {"Person": ["jdcrp__birthDate", "jdcrp__lifetime"]},
        ),
        "Death Dates": Topic(
            "Death dates of persons related to the cultural asset",
            {"Person": ["jdcrp__deathDate", "jdcrp__lifetime"]},
        ),
        "CCP Number": Topic(
            "CCP number of the cultural asset",
            {
                "CulturalAsset": [
                    "jdcrp__wccpNumber",
                    "jdcrp__marburgNumber",
                    "jdcrp__munichNumber",
                ]
            },
        ),
        "Bundesarchiv Metadata": Topic(
            "Band, signature, and title from the Bundesarchiv",
            {
                "CulturalAsset": [
                    "jdcrp__bundesarchivBand",
                    "jdcrp__bundesarchivSignature",
                    "jdcrp__bundesarchivTitle",
                    "jdcrp__bundesarchivStartDate",
                    "jdcrp__bundesarchivEndDate",
                ]
            },
        ),
        "All Identifiers": Topic(
            "All available identifiers of the cultural asset (CCP numbers, inventory numbers, etc.)",
            {
                "CulturalAsset": [
                    "jdcrp__wccpNumber",
                    "jdcrp__marburgNumber",
                    "jdcrp__munichNumber",
                    "jdcrp__errNumber",
                    "jdcrp__linzNumber",
                    "jdcrp__inventoryNumber",
                    "jdcrp__catalogNumber",
                    "jdcrp__negativeNumber",
                    "jdcrp__claimNumber",
                    "jdcrp__shelfNumber",
                ]
            },
        ),
        "Deposit": Topic(
            "Information about the deposit of the cultural asset",
            {"DepositionEvent": []},
        ),
        "Transfer": Topic(
            "Information about the transfer of the cultural asset",
            {"TransferEvent": []},
        ),
        "Acquisition": Topic(
            "Information about the acquisition of the cultural asset",
            {"AcquisitionEvent": []},
        ),
        "Confiscation": Topic(
            "Information about the confiscation of the cultural asset",
            {"ConfiscationEvent": []},
        ),
    }


def get_basic_search_topic() -> Topic:
    """
    Attributes to be searched with the basic, free-text search mode.
    """

    return Topic(
        "",
        {
            "CulturalAsset": [],  # An empty list signals that all attributes of the entity should be searched
            "Person": [],
        },
    )
