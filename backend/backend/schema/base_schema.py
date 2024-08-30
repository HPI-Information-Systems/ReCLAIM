"""
Contains all base schemas.
"""

import enum
from typing import Annotated, Generic, List, Optional, TypeVar, Dict

from pydantic import BaseModel, Field


class SupportedSource(enum.Enum):
    """
    Enum for the different sources.
    """

    ###
    # NOTICE: When modifying this enum, please make sure to also update the frontend's getSourceName function
    # located in frontend/src/lib/hooks/getSourceFromSourceAttribute.ts
    ###

    ERR = "err"  # Einsatzstab Reichsleiter Rosenberg
    WCCP = "wccp"  # Wiesbaden Central Collection Point
    LINZ = "linz"  # Sonderauftrag Linz
    MCCP = "munich"  # Munich Central Collection Point
    MACCP = "marburg"  # Marburg Central Collection Point
    GOER = "goer"  # Hermann Göring Collection


class EntityModel(BaseModel):
    """
    Base class for all models. Used to define common attributes.
    """

    id: str
    source_id: SupportedSource


class TaxonomyModel(BaseModel):
    """
    Base class for all taxonomies. Used to define common attributes.
    """

    id: str


EntryType = TypeVar("EntryType")


class Entry(BaseModel, Generic[EntryType]):
    """
    Contains the raw and parsed value of an attribute.
    """

    raw: Dict[str, EntryType]
    parsed: EntryType


ResultType = TypeVar("ResultType")


class SearchResults(BaseModel, Generic[ResultType]):
    """
    Contains the results of a search query, including the total count of results.
    """

    results_match_all_search_filters: List[ResultType]
    results_match_some_search_filters: List[ResultType]
    total_count_match_all_search_filters: int
    total_count_match_some_search_filters: int


EntityType = TypeVar("EntityType")


class SimilarEntity(BaseModel, Generic[EntityType]):
    """
    Represents a similarity edge to another entity with a number indicating the confidence.
    """

    entity: EntityType
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
