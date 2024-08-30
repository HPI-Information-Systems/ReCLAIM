import os
from seed.neo4j_interaction import (
    ingest_ttl,
    setup_namespaces,
    read_data,
    get_db_driver,
)


def import_source(file_name: str):
    driver = get_db_driver()

    with driver.session() as session:

        print("Setting up namespaces:")
        namespaces = read_data(
            os.path.join(os.getcwd(), "seed", "data", "namespaces.ttl")
        )
        session.execute_write(setup_namespaces, namespaces)

        print(f"Started importing data from {file_name}")

        session.execute_write(
            ingest_ttl, read_data(os.path.join(os.getcwd(), "seed", "data", file_name))
        )


if __name__ == "__main__":
    file_name = input('Type the filename to import from "seed/data/" => ')
    import_source(file_name)
