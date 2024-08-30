"""
Contains all routes for fetching and searching through persons
"""

from typing import Annotated, List
from backend.db_crud.search import SearchEntityType, search
from backend.schema import SearchResults, Person
from backend.schema.extensions import PersonExtension
from fastapi import APIRouter, Depends, Query, status
from neo4j import Session

from backend.db_crud.person import fetch_by_id

from ..dependencies.db import with_db

router = APIRouter(prefix="/person", tags=["Person"])


@router.get("/getById", status_code=status.HTTP_200_OK)
def get_by_id(id: str, session: Session = Depends(with_db)) -> PersonExtension:
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
) -> SearchResults[Person]:
    return search(q, SearchEntityType.Person, limit, cursor, session)
