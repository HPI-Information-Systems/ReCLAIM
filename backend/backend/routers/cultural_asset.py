"""
Contains all routes for fetching and searching through cultural assets
"""

from typing import Annotated, Dict, List

from backend.db_crud.search import SearchEntityType, search
from backend.schema import SearchResults, CulturalAsset
from backend.schema.extensions import CulturalAssetExtension
from backend.topics import get_cultural_asset_topics
from fastapi import APIRouter, Depends, HTTPException, Query, status
from neo4j import Session

from backend.db_crud.cultural_asset import fetch_by_id
from backend.schema import CulturalAsset

from ..dependencies.db import with_db

router = APIRouter(prefix="/culturalAsset", tags=["CulturalAsset"])


@router.get("/getById", status_code=status.HTTP_200_OK)
def get_by_id(id: str, session: Session = Depends(with_db)) -> CulturalAssetExtension:
    """
    Returns all data of a cultural asset by its id.
    """

    cultural_asset = fetch_by_id(id, session=session)

    if not cultural_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cultural asset with id '{id}' not found",
        )

    return cultural_asset


@router.get("/search", status_code=status.HTTP_200_OK)
def fulltext_search(
    q: Annotated[
        List[str],
        Query(
            description="Search query. This parameter can be set multiple times to filter by multiple search terms. The format for query terms is q=[!][topic]|<search_text>. Each field is separated by a delimiter, a pipe (|). Example query: /search?q=!Title|Portrait&q=Person+Names|Picasso results in a search for all assets whose title does not contain 'Portrait' and the name of any related person contains 'Picasso'."
        ),
    ],
    sources: Annotated[
        List[str],
        Query(
            description="List of sources to search in. If not provided, all sources are searched."
        ),
    ] = None,
    onlyWithImages: bool = None,
    limit: int = 100,
    cursor: int = 0,
    session: Session = Depends(with_db),
) -> SearchResults[CulturalAsset]:
    return search(
        q,
        SearchEntityType.CulturalAsset,
        limit,
        cursor,
        session,
        filters={"sources": sources, "onlyWithImages": onlyWithImages},
    )


@router.get("/topics", status_code=status.HTTP_200_OK)
def get_topics() -> (
    Dict[str, str]
):  # Returns a dictionary with key: topic name, value: topic tooltip
    return {
        topic_name: topic.tooltip
        for topic_name, topic in get_cultural_asset_topics().items()
    }
