"""
Contains routes for serving typing suggestion features.
"""

import re
from typing import List

from backend.db_crud.input_sanitization import sanitize_cypher_query_label
from backend.db_crud.search import get_lucene_query
from backend.topics import get_basic_search_topic, get_cultural_asset_topics
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Session

from ..dependencies.db import with_db

router = APIRouter(prefix="/autocomplete", tags=["Autocomplete"])


@router.get("/completions", status_code=status.HTTP_200_OK)
def fetch_autocomplete_completions(
    q: str,
    topic: str,
    limit: int = 10,
    session: Session = Depends(with_db),
) -> List[str]:
    """
    Returns a list of autocomplete suggestions for the given query.
    """

    cultural_asset_topic = None
    if topic:
        cultural_asset_topic = get_cultural_asset_topics().get(topic)
    else:
        cultural_asset_topic = get_basic_search_topic()

    if cultural_asset_topic is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid search topic: " + topic,
        )

    topic_cypher_queries: list[str] = []
    query_params = {}
    subquery_id = 0

    for entity_type, attributes in cultural_asset_topic.searched_attributes.items():
        param_name_q = f"q_{str(subquery_id)}"
        query_params[param_name_q] = f"(?i).*{re.escape(q)}.*"

        if len(attributes) == 0:
            cypher_query = f"""
                MATCH (node:jdcrp__{entity_type})
                UNWIND keys(node) AS key
                WITH key, node
                WHERE NOT key IN ['uri', 'jdcrp__derivedUsingMapping'] 
                AND node[key] =~ ${param_name_q}
                RETURN DISTINCT node[key] AS suggestion 
                LIMIT $limit
            """
            topic_cypher_queries.append(cypher_query)
        else:
            for attribute in attributes:
                cypher_query = f"""
                    MATCH (node:jdcrp__{entity_type}) 
                    WHERE node.{attribute} =~ ${param_name_q}
                    RETURN DISTINCT node.{attribute} AS suggestion 
                    LIMIT $limit
                """
                topic_cypher_queries.append(cypher_query)

        subquery_id += 1

    if len(topic_cypher_queries) == 0:
        return []

    autocomplete_query = (
        "CALL {"
        + " UNION ALL ".join(topic_cypher_queries)
        + "}"
        + """
        RETURN DISTINCT suggestion LIMIT $limit
        """
    )

    db_response = session.run(
        autocomplete_query,
        **query_params,
        limit=limit,
    )
    return [str(record[0]) for record in db_response]
