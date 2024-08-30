import pandas as pd
from neo4j import Session


def ingest_match(uri1: str, uri2: str, confidence: float, neo4j_session: Session):
    """
    Ingests a single match into the database.
    """
    neo4j_session.run(
        """
            MATCH (n:jdcrp__CulturalAsset {uri: $uri_from}) MATCH (m:jdcrp__CulturalAsset {uri: $uri_to})
            CREATE (n)-[:jdcrp__similarEntity {jdcrp__confidence: $confidence}]->(m)
        """,
        uri_from=uri1,
        uri_to=uri2,
        confidence=confidence,
    )


def ingest_matches_batch(matches: pd.DataFrame, neo4j_session: Session):
    """
    Ingests a batch of matches into the database.
    """
    for i, match in matches.iterrows():
        ingest_match(match["uri1"], match["uri2"], match["confidence"], neo4j_session)

        print(f"Match {i+1} of {len(matches)} ingested.")
