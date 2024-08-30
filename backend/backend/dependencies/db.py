"""
    This file contains the database connection and the dependency injection for it..
"""


from neo4j import GraphDatabase

from ..config import get_settings

settings = get_settings()

DRIVER = GraphDatabase.driver(
    uri=settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
)


def with_db():
    """
    Primary dependency injection for a database session.
    """
    with DRIVER.session() as session:
        yield session
