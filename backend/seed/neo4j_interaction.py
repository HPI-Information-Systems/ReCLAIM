from neo4j import ManagedTransaction, GraphDatabase

from backend.config import get_settings

def get_db_driver():
    settings = get_settings()
    return GraphDatabase.driver(
        settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
    )

def read_data(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
    return data


def ingest_ttl(tx: ManagedTransaction, data: str):
    query = """CALL n10s.rdf.import.inline($data,"Turtle")"""
    tx.run(query, data=data, limit=1000)


def setup_namespaces(tx: ManagedTransaction, data:str):
    tx.run("""CALL n10s.nsprefixes.addFromText($data)""", data=data)
