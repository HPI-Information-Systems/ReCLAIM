from backend.parsing.similar_entities.extract_similar_entities import (
    extract_similar_entities_from_db_response,
)
from backend.parsing.events.extract_events import extract_events_from_db_response
from backend.schema.extensions import CulturalAssetExtension
from fastapi import Depends
from neo4j import Session

from backend.dependencies.db import with_db
from backend.parsing.utility import build_entity_uri_from_id, extract_source_id_from_uri
from backend.schema import CulturalAsset
from backend.parsing.entity_parser import extract_entity_data_from_db_response


def fetch_by_id(
    id: str, session: Session = Depends(with_db)
) -> CulturalAssetExtension | None:
    """
    Retrieves a cultural asset by its id.
    """

    uri = build_entity_uri_from_id(id, "CulturalAsset")

    # This cypher query consists of the following independent steps:
    # 1. Retrieve the Cultural Asset with the URI queried, together with its related objects
    # 2. Retrieve all similar Cultural Assets, along with their images
    cultural_asset_data = session.run(
        """
            MATCH (cultural_asset:jdcrp__CulturalAsset)
            WHERE cultural_asset.uri = $uri
            OPTIONAL MATCH (cultural_asset)-[relation]->(related_object)
            OPTIONAL MATCH (related_object)-[:jdcrp__derivedFrom]->(related_object_record)
            WITH
                cultural_asset,
                COLLECT({
                    relation: type(relation),
                    related_entity: {
                        attributes: properties(related_object),
                        derived_from_record: properties(related_object_record)
                    }
                }) as relations

            OPTIONAL MATCH (cultural_asset)-[similar_entity_edge:jdcrp__similarEntity]-(similar_cultural_asset)
            OPTIONAL MATCH (similar_cultural_asset)-[similar_cultural_asset_relation]->(similar_cultural_asset_related_object)
            OPTIONAL MATCH (similar_cultural_asset_related_object)-[:jdcrp__derivedFrom]->(similar_cultural_asset_related_object_record)
            WITH cultural_asset, relations, similar_cultural_asset, similar_entity_edge,
                COLLECT({
                    relation: type(similar_cultural_asset_relation),
                    related_entity: {
                        attributes: properties(similar_cultural_asset_related_object),
                        derived_from_record: properties(similar_cultural_asset_related_object_record)
                    }
                }) AS similar_cultural_asset_relations
            WITH cultural_asset, relations,
                COLLECT({
                    attributes: properties(similar_cultural_asset),
                    relations: similar_cultural_asset_relations,
                    confidence: similar_entity_edge.jdcrp__confidence
                }) AS similar_cultural_assets

            OPTIONAL MATCH (event)-[:jdcrp__affectedCulturalAsset]->(cultural_asset)
            OPTIONAL MATCH (event)-[:jdcrp__derivedFrom]->(event_record)
            OPTIONAL MATCH (event)-[event_relation]->(event_related_entity)
            WITH cultural_asset, relations, similar_cultural_assets, event, COLLECT({
                relation: type(event_relation),
                related_entity: {
                    attributes: properties(event_related_entity),
                    derived_from_record: properties(event_record)
                }
            }) AS event_related_entities
            WITH cultural_asset, relations, similar_cultural_assets, COLLECT({
                event_type: CASE WHEN labels(event)[0] STARTS WITH "jdcrp" THEN labels(event)[0] ELSE labels(event)[1] END,
                attributes: properties(event),
                relations: event_related_entities
            }) as events

            RETURN
                properties(cultural_asset) AS attributes,
                relations,
                similar_cultural_assets,
                events;
        """,
        uri=uri,
    ).data()

    # Return none if no result for given id.
    if len(cultural_asset_data) == 0:
        return None
    else:
        cultural_asset_data = cultural_asset_data[0]

    return CulturalAssetExtension(
        cultural_asset=CulturalAsset(
            id=id,
            source_id=extract_source_id_from_uri(uri),
            **extract_entity_data_from_db_response(CulturalAsset, cultural_asset_data),
        ),
        similar_cultural_assets=extract_similar_entities_from_db_response(
            CulturalAsset, cultural_asset_data["similar_cultural_assets"]
        ),
        events=extract_events_from_db_response(cultural_asset_data["events"]),
    )
