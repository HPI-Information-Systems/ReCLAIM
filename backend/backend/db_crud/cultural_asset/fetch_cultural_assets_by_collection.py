from math import ceil
from typing import Any, Dict, List

from backend.parsing.entity_parser.collection import extract_related_cultural_asset_list
from neo4j import Session

from backend.parsing.utility import (
    build_entity_uri_from_id,
)
from backend.schema.base_schema import SupportedSource

from ...schema import CulturalAsset


def fetch_cultural_assets_by_collection_id(
    collection_id: str, session: Session, page: int, page_size: int
) -> List[CulturalAsset]:

    uri = build_entity_uri_from_id(collection_id, "Collection")

    query = """
        MATCH (collection:jdcrp__Collection)-[r:jdcrp__collectedIn]-(entity:jdcrp__CulturalAsset)
        WHERE collection.uri = $uri
        WITH collection, entity
        CALL {
            WITH collection
            MATCH (collection)-[:jdcrp__collectedIn]-(countEntity:jdcrp__CulturalAsset)
            RETURN COUNT(countEntity) AS total_count
        }
        RETURN
            entity {.*} AS attributes,
            total_count
        SKIP $offset
        LIMIT $page_size
    """
    print(page_size, page * page_size)
    result = session.run(
        query, uri=uri, page_size=page_size, offset=(page - 1) * page_size
    ).data()

    entities = extract_related_cultural_asset_list(result)

    total_count = result[0]["total_count"]

    return {
        "entities": entities,
        "total_page_count": ceil(total_count / page_size),
        "total_result_count": total_count,
    }
