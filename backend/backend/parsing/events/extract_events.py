from typing import Any, Dict, List

from backend.schema import *
from backend.parsing.utility import (
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)
from backend.parsing.entity_parser import (
    extract_attributes_from_db_response,
    extract_relations_from_db_response,
    extract_record_from_db_response,
)


def extract_events_from_db_response(db_event_data: List[Dict[str, Any]]) -> List[Dict]:
    """
    Extracts the events from the neo4j response for the cultural_asset fetch_by_id query.
    :param db_event_data: The neo4j response data of the events.
    :return: A list of dictionaries containing the extracted events.
    """

    event_list = []

    if len(db_event_data) == 1 and db_event_data[0]["attributes"] is None:
        return []

    for event_data in db_event_data:
        event_data["relations"] = [
            relation
            for relation in event_data["relations"]
            if relation["relation"] != "jdcrp__affectedCulturalAsset"
        ]
        derived_from_record = extract_record_from_db_response(event_data["relations"])
        event_type = event_data["event_type"].split("__")[1]
        event_class = globals()[event_type]

        event = {
            "id": extract_entity_id_from_uri(event_data["attributes"]["uri"]),
            "source_id": extract_source_id_from_uri(event_data["attributes"]["uri"]),
            "relative_order": event_data["attributes"].pop(
                "jdcrp__relativeOrder", None
            ),
        }

        extract_attributes_from_db_response(
            event, event_data["attributes"], derived_from_record
        )

        extract_relations_from_db_response(
            event,
            event_class,
            event_data["relations"],
            derived_from_record,
            event_data["attributes"]["jdcrp__derivedUsingMapping"],
        )

        event_list.append(event_class(**event))

    return event_list
