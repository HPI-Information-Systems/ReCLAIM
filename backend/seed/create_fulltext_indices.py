###
# Using the schema turtle file, this script executes the Cypher commands to create the per-entity fulltext indices for the Neo4j database.
# The primary fulltext index indexes all literal properties which are defined in the ontology (i.e. properties with range prefixed xsd:)
###

import os
from rdflib import Namespace
from neo4j import GraphDatabase
from backend.config import get_settings
from ontology_parse_properties import get_structured_class_properties_from_ontology
from rdflib import Namespace

jdcrp = Namespace("https://graph.jdcrp.org/schema#")

# Specify properties to exclude from indexing
exclude_properties = [
    jdcrp.derivedFrom,
    jdcrp.derivedUsingMapping,
    jdcrp.url,  # Image URLs are not indexed
]


def get_project_root() -> str:
    """
    Returns the project root folder.
    Assumption: The project root itself is not located in a subfolder containing in the name 'kunstgraph'.
    """
    return os.path.abspath(__file__).split("kunstgraph")[0] + "kunstgraph"


def create_fulltext_indices():
    settings = get_settings()
    driver = GraphDatabase.driver(
        settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
    )
    structured_properties = get_structured_class_properties_from_ontology(
        ignore_properties=exclude_properties
    )

    for class_uri, properties in structured_properties.items():
        class_name = class_uri.removeprefix(jdcrp)
        cypher_command = f"CREATE FULLTEXT INDEX {class_name}FulltextIndex FOR (n:jdcrp__{class_name}) ON EACH [{','.join([f'n.jdcrp__{p}' for p in properties.keys()])}]"

        with driver.session() as session:
            session.execute_write(lambda tx: tx.run(cypher_command))
        print(f"Created {class_name}FulltextIndex.")


if __name__ == "__main__":
    create_fulltext_indices()
