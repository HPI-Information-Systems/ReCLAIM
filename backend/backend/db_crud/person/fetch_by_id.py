from typing import Any, Dict, List

from fastapi import Depends
from neo4j import Session

from backend.dependencies.db import with_db
from backend.parsing.entity_parser import extract_entity_data_from_db_response
from backend.parsing.similar_entities.extract_similar_entities import (
    extract_similar_entities_from_db_response,
)
from backend.parsing.utility import (
    build_entity_uri_from_id,
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)
from backend.schema import Collection, CulturalAsset, Person, SupportedSource
from backend.schema.extensions import PersonExtension


def extract_related_cultural_asset_list(
    cultural_assets_data: List[Dict[str, Any]]
) -> List[CulturalAsset]:
    cultural_asset_list = []
    for cultural_asset_data in cultural_assets_data:
        if cultural_asset_data["attributes"] is None:
            continue

        cultural_asset = CulturalAsset(
            id=extract_entity_id_from_uri(cultural_asset_data["attributes"]["uri"]),
            source_id=SupportedSource(
                extract_source_id_from_uri(cultural_asset_data["attributes"]["uri"])
            ),
            **extract_entity_data_from_db_response(CulturalAsset, cultural_asset_data),
        )
        cultural_asset_list.append(cultural_asset)

    return cultural_asset_list if cultural_asset_list else []


def extract_related_collection_list(
    collections_data: List[Dict[str, Any]]
) -> List[Collection]:
    collection_list = []
    for collection_data in collections_data:
        if collection_data["attributes"] is None:
            continue

        collection = Collection(
            id=extract_entity_id_from_uri(collection_data["attributes"]["uri"]),
            source_id=SupportedSource(
                extract_source_id_from_uri(collection_data["attributes"]["uri"])
            ),
            **extract_entity_data_from_db_response(Collection, collection_data),
        )
        collection_list.append(collection)

    return collection_list if collection_list else []


def fetch_by_id(id: str, session: Session = Depends(with_db)) -> PersonExtension | None:
    """
    Retrieves a person by their id.
    """

    uri = build_entity_uri_from_id(id, "Person")

    # This cypher query consists of the following independent steps:
    # 1. Retrieve the Person with the URI queried, together with its related objects
    # 2. Retrieve all Cultural Assets, along with its images, which the Person created
    # 3. Retrieve all Cultural Assets, along with its images, which the Person owned
    # 4. Retrieve all Collections which the person owned
    # 5. Retrieve all similar Persons
    person_data = session.run(
        """
            MATCH (person:jdcrp__Person)
            WHERE person.uri = $uri
            OPTIONAL MATCH (person)-[relation]->(related_object)
            OPTIONAL MATCH (related_object)-[:jdcrp__derivedFrom]->(related_object_record)
            WITH
                person,
                COLLECT({
                    relation: type(relation),
                    related_entity: {
                        attributes: properties(related_object),
                        derived_from_record: properties(related_object_record)
                    }
                }) AS relations

            OPTIONAL MATCH (cultural_asset_created_by:jdcrp__CulturalAsset)-[:jdcrp__createdBy]->(person)
            OPTIONAL MATCH (cultural_asset_created_by)-[cultural_asset_created_by_image_relation]->(cultural_asset_created_by_image:jdcrp__Image)

            WITH person, relations, cultural_asset_created_by,
                COLLECT({
                    relation: type(cultural_asset_created_by_image_relation),
                    related_entity: {
                        attributes: properties(cultural_asset_created_by_image)
                    }
                }) AS cultural_asset_created_by_image_relations

            WITH person, relations,
                COLLECT({
                    attributes: properties(cultural_asset_created_by),
                    relations: cultural_asset_created_by_image_relations
                }) AS cultural_assets_created_by

            OPTIONAL MATCH (cultural_asset_owned_by:jdcrp__CulturalAsset)-[:jdcrp__ownedBy]->(person)
            OPTIONAL MATCH (cultural_asset_owned_by)-[cultural_asset_owned_by_image_relation]->(cultural_asset_owned_by_image:jdcrp__Image)

            WITH person, relations, cultural_assets_created_by, cultural_asset_owned_by,
                COLLECT({
                    relation: type(cultural_asset_owned_by_image_relation),
                    related_entity: {
                        attributes: properties(cultural_asset_owned_by_image)
                    }
                }) AS cultural_asset_owned_by_image_relations

            WITH person, relations, cultural_assets_created_by,
                COLLECT({
                    attributes: properties(cultural_asset_owned_by),
                    relations: cultural_asset_owned_by_image_relations
                }) AS cultural_assets_owned_by

            OPTIONAL MATCH (collection_owned_by:jdcrp__Collection)-[:jdcrp__ownedBy]->(person)

            WITH person, relations, cultural_assets_created_by, cultural_assets_owned_by,
                COLLECT({
                    attributes: properties(collection_owned_by)
                }) AS collections_owned_by

            OPTIONAL MATCH (person)-[similar_entity_edge:jdcrp__similarEntity]-(similar_person)

            WITH person, relations, cultural_assets_created_by, cultural_assets_owned_by, collections_owned_by, similar_person, similar_entity_edge,
                COLLECT({
                    attributes: properties(similar_person),
                    confidence: similar_entity_edge.jdcrp__confidence
                }) AS similar_persons

            RETURN
                properties(person) AS attributes,
                relations,
                cultural_assets_created_by,
                cultural_assets_owned_by,
                collections_owned_by,
                similar_persons
        """,
        uri=uri,
    ).data()

    # Return none if no result for given id.
    if len(person_data) == 0:
        return None
    else:
        person_data = person_data[0]

    person = PersonExtension(
        person=Person(
            id=id,
            source_id=SupportedSource(extract_source_id_from_uri(uri)),
            **extract_entity_data_from_db_response(Person, person_data),
        ),
        cultural_assets_created=(
            extract_related_cultural_asset_list(
                person_data["cultural_assets_created_by"]
            )
        ),
        cultural_assets_owned=(
            extract_related_cultural_asset_list(person_data["cultural_assets_owned_by"])
        ),
        collections_owned=extract_related_collection_list(
            person_data["collections_owned_by"]
        ),
        similar_persons=extract_similar_entities_from_db_response(
            Person, person_data["similar_persons"]
        ),
    )

    return person
