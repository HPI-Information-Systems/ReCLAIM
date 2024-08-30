"""
Contains schema attributes which are not part of the ontology but are required in the backend schema as return types.
"""

from . import *


class CulturalAssetExtension(BaseModel):
    cultural_asset: CulturalAsset
    events: List[
        TransferEvent
        | ConfiscationEvent
        | AcquisitionEvent
        | DepositionEvent
        | RestitutionEvent
    ]
    similar_cultural_assets: List[SimilarEntity[CulturalAsset]]


class PersonExtension(BaseModel):
    person: Person

    similar_persons: List[SimilarEntity[Person]]
    cultural_assets_created: Optional[List[CulturalAsset]] = []
    cultural_assets_owned: Optional[List[CulturalAsset]] = []
    collections_owned: Optional[List[Collection]] = []


class AssetsInCollectionResults(BaseModel):
    entities: List[CulturalAsset]
    total_page_count: int
    total_result_count: int
