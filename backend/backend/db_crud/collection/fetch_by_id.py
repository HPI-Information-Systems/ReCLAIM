from backend.schema import Collection
from fastapi import Depends
from neo4j import Session

from backend.dependencies.db import with_db
from backend.parsing.utility import build_entity_uri_from_id, extract_source_id_from_uri
from backend.parsing.entity_parser import extract_entity_data_from_db_response


def fetch_by_id(id: str, session: Session = Depends(with_db)) -> Collection | None:
    """
    Retrieves a collection by its id.
    """

    uri = build_entity_uri_from_id(id, "Collection")

    collection_data = session.run(
        """
            MATCH (collection:jdcrp__Collection)
            WHERE collection.uri = $uri
            OPTIONAL MATCH (collection)-[relation]->(related_object)
            OPTIONAL MATCH (related_object)-[:jdcrp__derivedFrom]->(related_object_record)
            WITH
                collection,
                COLLECT({
                    relation: type(relation),
                    related_entity: {
                        attributes: properties(related_object),
                        derived_from_record: properties(related_object_record)
                    }
                }) as relations
            RETURN properties(collection) AS attributes, relations;
        """,
        uri=uri,
    ).data()

    # Return none if no result for given id.
    if len(collection_data) == 0:
        return None
    else:
        collection_data = collection_data[0]

    return Collection(
        id=id,
        source_id=extract_source_id_from_uri(uri),
        **extract_entity_data_from_db_response(Collection, collection_data)
    )
