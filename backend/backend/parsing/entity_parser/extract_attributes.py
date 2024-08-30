from backend.parsing.utility import (
    clean_neo4j_property_name,
    create_entity_entry,
    clean_derived_using_mapping,
    clean_record,
)


def extract_attributes_from_db_response(
    entity: dict,
    entity_attributes: dict,
    derived_from_record: dict | None,
):
    """
    This function receives a entity_attributes dictionary which contains the raw neo4j attribute data.
    It fills the given schema entity with the provided attribute data, according to the backend schema.

    :param entity: The entity to write the extracted attributes to.
    :param entity_types: The pydantic entity types
    :param entity_attributes: The raw neo4j attribute data.
    :param derived_from_record: The record from which the entity was derived as raw neo4j data.
    """

    # Prepares derived using mapping and record
    entity_attributes.pop("uri", None)
    derived_using_mapping = entity_attributes["jdcrp__derivedUsingMapping"]

    if derived_using_mapping is not None and derived_from_record is not None:
        derived_using_mapping = clean_derived_using_mapping(derived_using_mapping)
        derived_from_record = clean_record(derived_from_record)

    for key, value in entity_attributes.items():
        clean_key_name = clean_neo4j_property_name(key)
        if clean_key_name == "derived_using_mapping":
            continue

        entity[clean_key_name] = create_entity_entry(
            clean_key_name,
            value,
            derived_from_record,
            derived_using_mapping,
        )
