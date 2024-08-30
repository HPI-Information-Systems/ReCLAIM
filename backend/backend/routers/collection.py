"""
Contains all routes for fetching and searching through collections
"""

from typing import Annotated, List

from backend.schema.extensions import AssetsInCollectionResults
from fastapi import APIRouter, Depends, Query, status
from neo4j import Session

from pydantic import BaseModel

from backend.db_crud.collection import fetch_by_id
from backend.db_crud.cultural_asset.fetch_cultural_assets_by_collection import (
    fetch_cultural_assets_by_collection_id,
)
from backend.db_crud.search import SearchEntityType, search
from backend.schema import Collection, CulturalAsset, SearchResults

from ..dependencies.db import with_db

router = APIRouter(prefix="/collection", tags=["Collection"])


@router.get("/getById", status_code=status.HTTP_200_OK)
def get_by_id(id: str, session: Session = Depends(with_db)) -> Collection:
    return fetch_by_id(id=id, session=session)


@router.get("/search", status_code=status.HTTP_200_OK)
def fulltext_search(
    q: Annotated[
        List[str],
        Query(
            description="Search query. This parameter can be set multiple times to filter by multiple search terms. The format for query terms is q=[!][topic]|<search_text>. Each field is separated by a delimiter, a pipe (|). Example query: /search?q=!Title|Portrait&q=Person+Names|Picasso results in a search for all assets whose title does not contain 'Portrait' and the name of any related person contains 'Picasso'."
        ),
    ],
    limit: int = 100,
    cursor: int = 0,
    session: Session = Depends(with_db),
) -> SearchResults[Collection]:
    return search(q, SearchEntityType.Collection, limit, cursor, session)


@router.get("/getCulturalAssetsByCollectionId", status_code=status.HTTP_200_OK)
def get_cultural_assets_by_collection_id(
    id: str, page: int = 0, page_size: int = 100, session: Session = Depends(with_db)
) -> AssetsInCollectionResults:
    return fetch_cultural_assets_by_collection_id(
        collection_id=id, page=page, page_size=page_size, session=session
    )
