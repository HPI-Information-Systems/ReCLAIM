from typing import Type
from backend.parsing.entity_parser.extract_attributes import (
    extract_attributes_from_db_response,
)
from backend.parsing.entity_parser.extract_relations import (
    extract_relations_from_db_response,
)
from backend.parsing.utility import raise_unsupported_attr_error
from backend.schema import EntityModel


def extract_record_from_db_response(entity_relations: list) -> dict | None:
    """
    Extracts the record from the db response the entity is derived from.

    :param entity_relations: The entity relations field of the db response
    :return: The record
    """

    for relation in entity_relations:
        if relation["relation"] == "jdcrp__derivedFrom":
            derived_from_record = relation["related_entity"]
            entity_relations.remove(relation)
            if "attributes" not in derived_from_record:
                raise_unsupported_attr_error(
                    "Error: jdcrp__derivedFrom relation is missing an attributes field."
                )
            return derived_from_record["attributes"]

    return None


def entity_db_data_has_relations(entity_db_data: dict) -> bool:
    """
    Checks if the db response has relations.

    :param entity_db_data: The db response
    :return: True if the db response has relations, False otherwise
    """

    return "relations" in entity_db_data and entity_db_data["relations"] is not None


def extract_entity_data_from_db_response(
    entity_type: Type[EntityModel], entity_db_data: dict
) -> dict:
    """
    Creates an entity object from a db response.
    :param entity_type: The pydantic entity type to extract
    :param entity_db_data: The data retrieved from the neo4j database
    :return: The entity object

    Note that in order to use this extraction function, the entity_db_data dictionary should be in the following format. At least "attributes" or "relations" should exist:
    {
        "attributes": {
            "attribute1": "value1",
            "attribute2": "value2",
            ...
        },
        "relations": [
            {
                "relation": "relation_name1",
                "related_entity": {
                    "attributes": {
                        "uri": "uri1",
                        "attribute1": "value1",
                        ...
                    },
                    "derived_from_record": { ... }
                }
            },
            {
                "relation": "relation_name2",
                "related_entity": {
                    "attributes": {
                        "uri": "uri2",
                        "attribute1": "value1",
                        ...
                    },
                    "derived_from_record": { ... }
                }
            },
            ...
        ]
    }
    """

    entity = {}

    # Extract and set all attributes and relations that are reflected in the schema.
    derived_from_record = (
        extract_record_from_db_response(entity_db_data["relations"])
        if entity_db_data_has_relations(entity_db_data)
        else None
    )

    if entity_db_data["attributes"] is not None:
        extract_attributes_from_db_response(
            entity,
            entity_db_data["attributes"],
            derived_from_record,
        )

    if entity_db_data_has_relations(entity_db_data):
        extract_relations_from_db_response(
            entity,
            entity_type,
            entity_db_data["relations"],
            derived_from_record,
            (
                entity_db_data["attributes"].get("jdcrp__derivedUsingMapping", None)
                if entity_db_data["attributes"] is not None
                else None
            ),
        )

    return entity
