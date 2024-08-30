import os
from seed.neo4j_interaction import (
    get_db_driver,
    read_data,
    ingest_ttl,
    setup_namespaces,
)
from seed.create_fulltext_indices import create_fulltext_indices


def seed():
    """
    Seeds the database with the ttl files in the seed/data folder.
    """

    driver = get_db_driver()

    with driver.session() as session:
        print(
            "Get yourself a coffee, because ... this won't take as long, but still, coffee tastes good."
        )

        print("Started to remove all entities from the database.")
        session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n;"))
        session.execute_write(lambda tx: tx.run("CALL apoc.schema.assert({}, {})"))

        print("Started to create unqiue constraints and graph config.")
        # Create constraints
        session.execute_write(
            lambda tx: tx.run(
                "CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;"
            )
        )
        session.execute_write(lambda tx: tx.run("CALL n10s.graphconfig.init();"))

        print("Started to setup namespaces.")
        namespace_data = read_data(
            os.path.join(os.path.dirname(__file__), "data", "namespaces.ttl")
        )
        session.execute_write(setup_namespaces, namespace_data)

        ttl_files = os.listdir(os.path.join(os.path.dirname(__file__), "data"))

        # Ingest ttl files
        for ttl_file in ttl_files:
            if ttl_file == "namespaces.ttl":
                continue
            print(f"Started import of {ttl_file}")
            session.execute_write(
                ingest_ttl,
                read_data(os.path.join(os.path.dirname(__file__), "data", ttl_file)),
            )


if __name__ == "__main__":
    seed()
    print("Finished data import.")
    print("Creating fulltext indices.")
    create_fulltext_indices()
    print("Finished creating fulltext indices.")
