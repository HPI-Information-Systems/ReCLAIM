from typing import Any, Dict, List, Type

from backend.parsing.entity_parser.create_entity import (
    extract_entity_data_from_db_response,
)
from backend.parsing.utility import (
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)
from backend.schema.base_schema import SimilarEntity


def extract_similar_entities_from_db_response(
    entity_type: Type, similar_entity_data: List[Dict[str, Any]]
) -> List[SimilarEntity]:
    """
    Returns a structured List[SimilarEntity] from the neo4j similarity data.

    :param entity_type: The type of entity to be extracted.
    :param similar_entity_data: The neo4j data to extract.
    :return: A structured List[SimilarEntity] from the neo4j similarity data.
    """
    similar_entity_return_list = []

    for similar_entity in similar_entity_data:
        if similar_entity["attributes"] is not None:
            similar_entity_uri = similar_entity["attributes"]["uri"]
            similar_entity_return_list.append(
                SimilarEntity[entity_type](
                    entity=entity_type(
                        id=extract_entity_id_from_uri(similar_entity_uri),
                        source_id=extract_source_id_from_uri(similar_entity_uri),
                        **extract_entity_data_from_db_response(
                            entity_type, similar_entity
                        ),
                    ),
                    confidence=similar_entity["confidence"],
                )
            )
    return similar_entity_return_list
