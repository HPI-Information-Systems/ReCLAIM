"""
    Setup for pytest. This file is automatically loaded first by pytest.
"""

import pytest
from fastapi.testclient import TestClient
from neo4j import GraphDatabase
from pydantic_settings import SettingsConfigDict

from backend.config import Settings
from backend.dependencies.db import with_db
from backend.main import app

Settings.model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")

settings = Settings()


def override_with_db():
    """
    Overrides the database connection with the test database.
    """

    with GraphDatabase.driver(
        uri=settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
    ) as driver:

        with driver.session() as session:
            yield session


@pytest.fixture
def with_client():
    """
    Generates a testclient for querying the FastAPI app. Only works for synchronous routes.
    For asynchronous routes, create a fixture using httpx.
    """

    app.dependency_overrides[with_db] = override_with_db
    client = TestClient(app)

    yield client
