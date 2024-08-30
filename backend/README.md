# ReCLAIM Backend

This directory contains all code of the ReCLAIM backend service. The backend service is responsible for receiving requests from the frontend, validating requests, querying the Neo4j graph database and sending appropriate responses back to the frontend.

## Table of Contents
- [Installation](#installation)
    - [1. Install poetry](#1-install-poetry)
    - [2. Install dependencies](#2-install-dependencies)
    - [3. Run the server](#3-run-the-server)
    - [4. Initializing the database](#4-initializing-the-database)
    - [5. Configure environment variables](#5-configure-environment-variables)
    - [6. Seed the database](#6-seed-the-database)
    - [7. Generate backend schema](#7-generate-backend-schema)
- [Backend Tech-Stack](#backend-tech-stack)
- [Scripts](#scripts)
- [Structure](#structure)

## Installation

<strong>Notice: All command listings in this README are always executed inside the `backend` folder.</strong> 

### 1. Install Poetry

We're using [Poetry](https://python-poetry.org/) to manage our backend dependencies.

You can find installation instructions for Poetry [here](https://python-poetry.org/docs/#installing-with-the-official-installer).

<strong>Important: Do not use pip!</strong> Poetry is a replacement for pip. Whenever you want to install additional packages, run `poetry add XXX`.

### 2. Install dependencies

To install all backend dependencies, run:

```bash
poetry install
```

### 3. Run the server

To run the backend server, in the backend folder, run:

`npm run dev`

### 4. Initializing the database

For development and testing, we use a locally hosted instance of the neo4j database. These are hosted via docker.

To start the development database, run `npm run db:up`. To stop it, run `npm run db:down`. There is additionally a test database which should be used for running tests. To start the test database, run `npm run testdb:up`. To stop it, run `npm run testdb:down`.

When the neo4j database server is up and running, you should be able to reach the browser interface at http://localhost:7474/browser/.

<strong>Important!</strong> Unexpectedly shutting down the docker container by closing the terminal seems to destroy the docker container. Therefore, it is recommended to use `npm run db:down` for shutting down the container.

### 5. Configure environment variables

Before seeding the database, you should set the `NEO4J_URI`, `NEO4J_USERNAME` and `NEO4J_PASSWORD` environment variables in the `/backend/.env` file. When using a local neo4j database instance, you can look up these credentials in the docker configuration at `/backend/docker-compose.yml`. However, you can also connect to any other neo4j instance, for example to the production database.
```bash
NEO4J_URI=neo4j://<server_address>:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>
```

### 6. Seed the database

When the database has been started, data can be imported. For importing the data you can use the seeding scripts in `/backend/seed`.

**Quick seeding**

If you just want to quickly seed the database with all available source data, you can just run `poetry run python ./seed/run_etl_and_seed.py`. This script will run the ETL pipeline to prepare the data and automatically import all files into the neo4j database instance.

**Manual Seeding**

If you want to only import a selected set of sources, you should follow the instructions below.

The seeding script imports all `.ttl` files from the `/backend/seed/data` directory into the database. Therefore, this directory should always contain the `namespaces.ttl`, `material.ttl` and `classification.ttl` files. `namespaces.ttl` contains all source prefixes for `.ttl` files and must be updated when new sources are integrated in the platform. `material.ttl` and `classification.ttl` contain taxonomy entities that are equal across sources. They can also be found in `/ontology/taxonomies`. Be sure that the latest taxonomy `.ttl` files are included in `/backend/seed/data` before running the seeding scripts.

For importing actual source data, you must first generate the corresponding `.ttl` files using the ETL-pipeline. See `/etl/README.md` on how to do this. Afterwards, you need to copy the created `.ttl` source files that you wish to important into the `/backend/seed/data` directory.

When all `.ttl` source files are included in `/backend/seed/data`, you can run either run `poetry run python ./seed/seed_database.py` to import all source files or just run `poetry run python ./seed/import_source.py` to only import a specific source file.

**Re-seed database**
Except for the script importing individual sources, the seeding scripts run a Cypher command to delete all entities that were stored in the database prior to seeding new data. However, this mechanism fails for data amounts too large, since it is executed in a single transaction. Therefore, it is recommended to delete the database container instead. This is done by deleting its docker volume (use docker desktop app or `docker volume` command). Afterwards, start a fresh container to seed.

### Full-text Indices

For the platform's search feature, we use neo4j's built-in full-text indices. The indices must be created in order for the search to work. For each entity type, one index is created, indexing all its attributes.

**Create indices**

In case that either the quick seeding script `run_etl_and_seed.py` or the general seeding script `seed_database.py` was used, the index creation script is called automatically. You then see the creation of all indices in the console output.

In case you imported `.ttl` files manually and wish to create the indices, run `poetry run python ./seed/create_fulltext_indices.py`.

### 7. Generate backend schema

Finally, you need to generate the Pydantic backend schema from the RDF ontology. To do this, run `poetry run python ./generate_backend_schema.py`.

## Backend Tech-Stack
In this section, you can find an overview of the relevant libraries and frameworks used in the backend and how they work together.

- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a web framework for building APIs with Python based on standard Python type hints. With FastAPI we define API endpoints.
- [OpenAPI](https://www.openapis.org/) - FastAPI includes an OpenAPI module by default. We utilize this module, so you can access the OpenAPI documentation of the FastAPI server at https://localhost:8000.
- [Neo4j](https://neo4j.com/) - Neo4j is a graph database that stores our data in form of nodes (entities) and edges (relations).
- [Cypher](https://neo4j.com/docs/cypher-manual/current/introduction/) - Cypher is a query language built for Neo4j. We define Cypher queries as template strings in our FastAPI endpoints and send them to the neo4j instance.
- [Pydantic](https://docs.pydantic.dev/latest/) - Pydantic is a data validation library for Python. With Pydantic you can define a schema and data fields are validated when you instantiate objects from that schema. Therefore, we can assure that only correct data types are returned from our FastAPI service to the frontend. The Pydantic backend schema is automatically generated from the ontology defined in `/ontology`.
- [Docker](https://www.docker.com/) We use Docker for deployment of frontend, backend and of the neo4j database instance.

## Scripts
We defined a set of commands that you can use to quickly initialize and start servers in different modes. These commands are defined in `/backend/package.json` under the key `scripts`. To execute these scripts you need to have a recent version of [NPM](https://docs.npmjs.com/about-npm) installed. NPM automatically comes along with [Node](https://nodejs.org/en).

Then you can just run `npm run <script>` to run the corresponding script. E.g. `npm run db:up` will start the docker container that runs the database instance.

## Backend Modules
In this section we provide you with an overview of the different modules that make up our backend.

- `/backend/config/` defines a `Settings` class that is used to validate environment variables when initializing database connections. `/backend/dependencies/` is then used to create a driver object with the `Settings` for interaction with the database instance.
- `/backend/db_crud/` contains all functions running database queries for different entity types. E.g. `/backend/db_crud/cultural_asset/fetch_by_id.py` is used to retrieve a specific cultural asset entity from the database instance by id, and `/backend/db_crud/search.py` contains all code for running search queries against the neo4j database.
- `/backend/parsing/` contains functions for parsing neo4j database results into the defined Pydantic schema. We created a generic entity extractor that is capable of parsing the database result for an entity to its corresponding Pydantic format by extracting its attributes and relations.
- `/backend/routers/` contains the FastAPI endpoint definitions.
- `/backend/seed/` contains all functions for seeding the neo4j database instance as described in [Seed the Database](#6-seed-the-database).
- `/backend/tests/` contains a first setup for writing tests within FastAPI. However, backend tests are not yet utilized.
