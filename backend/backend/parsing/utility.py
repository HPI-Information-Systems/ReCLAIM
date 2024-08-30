from fastapi import HTTPException, status
import json


def camel_to_snake(name: str) -> str:
    """
    Converts a camelCase string to snake_case
    :param name: The camelCase string
    :return: The snake_case string
    """
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


def clean_neo4j_property_name(name: str) -> str:
    """
    Cleans the name of a Neo4j property to be conformant to the pydantic schemata
    E.g. jdcrp__name -> name | raw__name -> name
    :param name: The name of the property
    :return: The cleaned name
    """
    name = name[7:] if name.startswith("jdcrp__") else name
    name = name.split("__")[1] if name.startswith("raw_") else name

    name = camel_to_snake(name)

    return name


def extract_attribute_name_from_schema_uri(uri: str) -> str:
    """
    Extracts the <attribute_name> from a given schema uri. Expects the uri to be in the format:
    https://graph.jdcrp.org/schema#<attribute_name>
    :param uri: The schema uri
    :return: The attribute name
    """
    return uri.split("#")[1]


def extract_attribute_name_from_raw_uri(uri: str) -> str:
    """
    Extracts the <raw_attribute_name> from a given raw uri. Expects the uri to be in the format:
    https://graph.jdcrp.org/raw/<source_id>#<raw_attribute_name>
    :param uri: The raw uri
    :return: The raw attribute name
    """
    return uri.split("#")[-1]


def clean_derived_using_mapping(derived_using_mapping: str) -> dict:
    """
    Cleans the derived using mapping by extracting attribute names from the schema and record uris.
    :param derived_using_mapping: The derived using mapping
    :return: The cleaned derived using mapping
    """
    dum_dict = json.loads(derived_using_mapping)

    cleaned_dict = {}

    # Note that the derived_using_mapping is in the following format:
    # {
    #     "https://graph.jdcrp.org/schema#<attribute_name>": ["https://graph.jdcrp.org/raw/<source_id>#<raw_attribute_name>", ...],
    #     ...
    # }
    for key, value in dum_dict.items():
        cleaned_schema_attr = clean_neo4j_property_name(
            extract_attribute_name_from_schema_uri(key)
        )
        cleaned_raw_attr = []
        for raw_attr in value:
            cleaned_raw_attr.append(
                clean_neo4j_property_name(extract_attribute_name_from_raw_uri(raw_attr))
            )

        cleaned_dict[cleaned_schema_attr] = cleaned_raw_attr

    return cleaned_dict


def clean_record(record: dict) -> dict:
    """
    Cleans the record by cleaning attribute names.
    :param record: The record
    :return: The cleaned record
    """

    cleaned_dict = {}

    for key, value in record.items():
        cleaned_dict[clean_neo4j_property_name(key)] = value

    return cleaned_dict


def extract_source_id_from_uri(uri: str) -> str | None:
    """
    Extracts the <dataset> from a given uri. Expects the uri to be in the format
    https://graph.jdcrp.org/sources/<source_id>/<entity_type>#<entity_id>
    :param uri: The uri
    :return: The source id
    """

    return uri.split("/")[4]


def extract_entity_id_from_uri(uri: str) -> str:
    """
    Extracts the <entity_id> from a given uri. Expects the uri to be in the format
    https://graph.jdcrp.org/sources/<source_id>/<entity_type>#<entity_id>
    :param uri: The uri
    :return: The entity id
    """

    if uri.startswith("https://graph.jdcrp.org/taxonomies/"):
        taxonomy = uri.split("/")[-1]  # e.g. "classification#glass"
        return "_".join(taxonomy.split("#"))

    return extract_source_id_from_uri(uri) + "_" + uri.split("#")[1]


def extract_entity_type_from_uri(uri: str) -> str | None:
    """
    Extracts the <entity_type> from a given uri. Expects the uri to be in the format
    https://graph.jdcrp.org/sources/<source_id>/<entity_type>#<entity_id>
    or https://graph.jdcrp.org/taxonomies/<entity_type>#<entity_id> (in case of materials and classifications where None is returned)
    :param uri: The uri
    :return: The entity type
    """

    if uri.startswith("https://graph.jdcrp.org/taxonomies/"):
        return uri.split("/")[4].split("#")[0]

    return uri.split("/")[5].split("#")[0]


def build_entity_uri_from_id(entity_id: str, entity_type: str) -> str | None:
    """
    Builds the uri for an entity with a given entity type and id.
    TODO: Add support for Materials and Classifications
    """

    if entity_type == "Material" or entity_type == "Classification":
        print("Entity URI cannot be created for Material or Classification currently.")
        return None

    source_id = entity_id.split("_")[0]
    asset_id = entity_id[len(source_id) + 1 :]
    return f"https://graph.jdcrp.org/sources/{source_id}/{entity_type}#{asset_id}"


def create_entity_entry(
    key: str, value, record: dict, derived_using_mapping: dict
) -> dict | str:
    """
    Creates an entity entry object, which contains the raw and parsed values of an attribute.
    :param key: Attribute or relation name
    :param value: Corresponding value
    :param record: The raw record from which the entity was derived
    :param derived_using_mapping: The mapping used to derive the value
    :return: The Entry object
    """
    # TODO implement generalised approach to skip attributes not using derived_using_mapping
    if key == "url":
        return value

    if derived_using_mapping is None or record is None:
        return {"parsed": value, "raw": {}}

    raw_attribute_names = derived_using_mapping[key]

    raw_vals = {}
    for raw_attr in raw_attribute_names:
        if record.get(raw_attr) is not None:
            raw_vals[raw_attr] = record[raw_attr]

    return {"parsed": value, "raw": raw_vals}


def raise_unsupported_attr_error(error_message: str):
    """
    Raises an error if an unsupported attribute is encountered.
    """
    print(error_message)

    # Comment this out for debug
    """ raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=error_message,
    ) """
