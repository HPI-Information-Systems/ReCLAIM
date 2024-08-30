from backend.parsing.entity_parser.extract_attributes import (
    extract_attributes_from_db_response,
)
from backend.schema import *
from typing import Type
from backend.parsing.utility import (
    clean_derived_using_mapping,
    clean_neo4j_property_name,
    clean_record,
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)


def is_relation_of_type_list(
    entity_type: Type[EntityModel], relation_name: str
) -> bool:
    """
    This function checks if the relation type is of type List.

    :param entity_type: The entity type for which the relation type should be checked.
    :param relation_type: The relation type that should be checked.
    :return: True if the relation type is of type List, False otherwise.
    """

    related_entity_type = entity_type.__annotations__[relation_name].__args__[0]
    while hasattr(related_entity_type, "__args__"):
        if str(related_entity_type).startswith("typing.List"):
            return True
        related_entity_type = related_entity_type.__args__[0]

    return False


def extract_related_nontaxonomy_entity(
    related_entity_raw: dict,
) -> dict:
    """
    This function extracts the related non-taxonomy entity corresponding to the relation_type from the raw neo4j relation data.
    The entity cannot be a taxonomy entity (i.e. Classification, Material). For taxonomy entities, use extract_related_taxonomy_entity.

    :param related_entity_raw: The raw neo4j relation data of the related entity.
    :return: The extracted related entity.
    """

    related_entity_attributes = related_entity_raw["attributes"]
    related_entity_derived_from_record = related_entity_raw.get(
        "derived_from_record", None
    )

    related_entity_uri = related_entity_attributes["uri"]
    related_entity = {
        "id": extract_entity_id_from_uri(related_entity_uri),
        "source_id": SupportedSource(extract_source_id_from_uri(related_entity_uri)),
    }

    extract_attributes_from_db_response(
        related_entity,
        related_entity_attributes,
        related_entity_derived_from_record,
    )

    return related_entity


def extract_related_taxonomy_entity(
    taxonomy_entity_raw: dict,
    relation_name: str,
    derived_from_record: dict,
    derived_using_mapping: dict,
) -> dict:
    """
    This function extracts the related taxonomy entity corresponding to the relation_type from the raw neo4j relation data.
    The entity must be a taxonomy entity (i.e. Classification, Material). For non-taxonomy entities, use extract_related_nontaxonomy_entity.

    :param taxonomy_entity_raw: The raw neo4j relation data to extract.
    :param relation_name: The name of the relation (e.g. classified_as, consists_of_material).
    :param derived_from_record: The entity's raw record
    :param derived_using_mapping: The mapping from the pydantic entity type names to the raw attribute names of the record.
    :return: The extracted related entity.
    """

    related_entity_attributes = taxonomy_entity_raw["attributes"]
    related_entity_uri = related_entity_attributes.pop("uri")
    taxonomy_entity = {
        "id": extract_entity_id_from_uri(related_entity_uri),
    }

    for key, value in related_entity_attributes.items():
        clean_key_name = clean_neo4j_property_name(key)
        # if not one of the types in the related_entity_types list supports the attribute, raise an error
        if clean_key_name == "derived_using_mapping":
            continue

        if relation_name in derived_using_mapping:
            taxonomy_entity[clean_key_name] = {
                "raw": {
                    n: derived_from_record[n]
                    for n in derived_using_mapping[relation_name]
                },
                "parsed": value,
            }
        else:
            print(
                f"Error: No derived using mapping present for taxonomy relation {relation_name}. Affected uri: {related_entity_uri}"
            )
            taxonomy_entity[clean_key_name] = {
                "raw": [],
                "parsed": value,
            }

    return taxonomy_entity


def extract_related_entity(
    related_entity: dict,
    relation_name: str,
    derived_from_record: dict,
    derived_using_mapping: dict,
) -> dict:
    """
    This function extracts the related entity corresponding to the relation_type from the raw neo4j relation data.
    The entity can be a taxonomy entity (i.e. Classification, Material) or a non-taxonomy entity, the function determines the type and calls the appropriate extraction function.

    :param related_entity: The raw neo4j relation data of the related entity.
    :param relation_name: The name of the relation (e.g. classified_as, consists_of_material).
    :param derived_from_record: The entity's raw record
    :param derived_using_mapping: The mapping from the pydantic entity type names to the raw attribute names of the record.
    :return: The extracted related entity.
    """

    if "taxonomies" in related_entity["attributes"]["uri"]:
        return extract_related_taxonomy_entity(
            related_entity,
            relation_name,
            clean_record(derived_from_record),
            clean_derived_using_mapping(derived_using_mapping),
        )
    else:
        return extract_related_nontaxonomy_entity(related_entity)


def extract_relations_from_db_response(
    entity: dict,
    entity_type: Type,
    entity_relations: list[dict],
    derived_from_record: dict | None,
    derived_using_mapping: str,
):
    """
    This function receives a entity_relations dictionary which contains the raw neo4j relation data.
    It fills the given entity dict with the provided relation data, according to the backend schema.

    :param entity: The entity as a dict to write the extracted relations to.
    :param entity_type: The pydantic entity type to extract
    :param entity_relations: The raw neo4j relation data.
    :param derived_from_record: The entity's raw record
    :param derived_using_mapping: The mapping from the pydantic entity type names to the raw attribute names of the record.
    """

    entity_relation_dict = {}

    # Collect all entites of same relation type, create a list dynamically if multiple related entities are present
    for relation in entity_relations:
        if relation["relation"] is None or relation["related_entity"] is None:
            continue
        if relation["relation"] == "jdcrp__similarEntity":
            continue

        if entity_relation_dict.get(relation["relation"]) is None:
            entity_relation_dict[relation["relation"]] = relation["related_entity"]
        elif type(entity_relation_dict[relation["relation"]]) is not list:
            entity_relation_dict[relation["relation"]] = [
                entity_relation_dict[relation["relation"]],
                relation["related_entity"],
            ]
        else:
            entity_relation_dict[relation["relation"]].append(
                relation["related_entity"]
            )

    if len(entity_relation_dict) == 0:
        return

    # Extract and set all relations that are reflected in the schema
    for relation, related_entities in entity_relation_dict.items():
        relation_name = clean_neo4j_property_name(relation)

        if type(related_entities) is not list:
            # A single related entity
            related_entity = extract_related_entity(
                related_entities,
                relation_name,
                derived_from_record,
                derived_using_mapping,
            )

            # It is possible that the related entity is expected to be a list, but we only got a single element
            # In this case, we convert the single element to a list
            if is_relation_of_type_list(entity_type, relation_name):
                related_entity = [related_entity]

            entity[relation_name] = related_entity
        else:
            # Multiple related entities aggregated in a list
            related_entity_list = []

            for related_entity_raw in related_entities:
                related_entity_list.append(
                    extract_related_entity(
                        related_entity_raw,
                        relation_name,
                        derived_from_record,
                        derived_using_mapping,
                    )
                )
            entity[relation_name] = related_entity_list
