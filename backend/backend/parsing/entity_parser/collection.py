from typing import Any, Dict, List
from backend.parsing.entity_parser.create_entity import (
    extract_entity_data_from_db_response,
)
from backend.parsing.utility import (
    extract_entity_id_from_uri,
    extract_source_id_from_uri,
)
from backend.schema import CulturalAsset
from backend.schema.base_schema import SupportedSource


def extract_related_cultural_asset_list(
    cultural_assets_data: List[Dict[str, Any]]
) -> List[CulturalAsset]:
    cultural_asset_list = []
    for ca in cultural_assets_data:
        cultural_asset = CulturalAsset(
            id=extract_entity_id_from_uri(ca["attributes"]["uri"]),
            source_id=SupportedSource(
                extract_source_id_from_uri(ca["attributes"]["uri"])
            ),
            **extract_entity_data_from_db_response(CulturalAsset, ca),
        )
        cultural_asset_list.append(cultural_asset)

    return cultural_asset_list if cultural_asset_list else []
