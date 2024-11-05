# ReCLAIM monorepo
This monorepo contains all relevant code for the ReCLAIM platform.
The repository is structured into multiple packages.

### Demo Screencast
https://github.com/user-attachments/assets/c64d3d37-0646-41c0-94b3-0b827a466b3b

# Development

## Development setup

The monorepo uses turbo to manage the development environment. To install turbo, run the following command:

```bash
npm install turbo --global
```

To install all dependencies, run the following command:

```bash
turbo install
```

This will create the necessary virtual environments and install all dependencies.

Please also follow these steps:

1. Create a `.env` file in the project root, by copying the `.env.example` file. Fill in the necessary environment variables. **Do not check the .env file into a versioning system, as it may contain secret information**
2. Create symlinks into all subfolders. On a unix based system, you can use `ln -s ../.env .env` in each subfolder.
3. _(If you are using the centralized neo4j database, you can skip this step)_ <br>
   If you are using a local neo4j database, you can start it by running `docker-compose up dev_db` in the `backend` folder. For the search to work, the fulltext index must be created. Create it by running the following command in the `backend` folder: `poetry run python createPrimaryFulltextIndex.py`.

## Development workflow

To start the development environment, run the following command:

```bash
turbo dev
```

This will start the frontend and backend in development mode.

For streamlined development of both frontend and backend, we automatically generate a REST client for the backend API.
To generate the client explicitly, run the following command:

```bash
turbo run generate:client
```

This requires the backend to be running.

To also create a development instance of our neo4j database, either run `turbo db:up` to only start a detached neo4j database, or run `turbo dx` to start the database as well as starting the server.

## Usage of Pre-Commit

We use pre-commit to ensure that all code is formatted correctly. To install pre-commit, run the following command:

```bash
brew install pre-commit
```

using homebrew on MacOS, or

```bash
pip install pre-commit
```

otherwise.

To install the pre-commit hooks, run the following command:

```bash
pre-commit install
```

This will install the pre-commit hooks, which will run every time you commit code. If the hooks fail, the commit will be aborted. To run the hooks manually, run the following command:

```bash
pre-commit run --all-files
```

# Deployment

The project is hosted on our server at DHC-Lab. To deploy the latest version of the project from main and seed the database with the data from the current ETL scripts, log in to the server as root (type `sudo -i`), and type:

```bash
./deploy
```

To deploy without re-seeding the neo4j database and executing the ETL scripts, type:

```bash
./deploy_without_seed
```

The deployment script relies on the docker-compose.yml file being placed in the same directory, which defines network and volume information as well as the environment variables for the containers. Both the script and the docker-compose.yml should be placed **above** the project root.
The Dockerfiles for the frontend and backend are under kunstgraph/frontend/Dockerfile and kunstgraph/backend/Dockerfile respectively.

## Set up deployment on new server

Requirements:

- Python 3.12
- Poetry for Python

To set up the project for deployment on a new Linux server, make sure Python 3.12 is installed. Then, install Poetry for Python by running `curl -sSL https://install.python-poetry.org | python3 -` (refer to https://python-poetry.org/ for updates on the instructions, should they change). To clone the repository, it is recommended to add a GitHub ssh deploy key, such that the deployment scripts can fetch the repository.
It might be necessary to add poetry to PATH. Alternatively, run poetry using the explicit path.
After installation and cloning the project repository, install both the `backend` as well as the `etl` poetry projects in the `backend` project venv by running the following commands:

```bash
cd kunstgraph/backend
poetry install
poetry shell
cd ../etl
poetry install
exit
```

Copy the deployment scripts into the parent folder:

```bash
cp deploy deploy_without_seed ..
cd ..
chmod +x deploy
chmod +x deploy_without_seed
```

You can now simply deploy the newest version by running either `./deploy` or `./deploy_without_seed`.

## Default Password for neo4j
When deploying the neo4j docker instance, the password for the database access defaults to "PASSWORD" in this repo. To change it, change the NEO4J_PASSWORD environment variable both in the `deploy` script and `docker-compose.yml` file, as well as the NEO4J_AUTH password part in the `docker-compose.yml` file to your desired password.

# Packages

## Backend

The backend is a Python FastAPI application that provides an API to extract data from the Neo4j database and the ontology. The backend also provides an API to search for cultural assets and other entities.
You can find the backend code in the `backend` folder.
Instructions to run the backend can be found in the [README.md](backend/README.md) file.

## Frontend

The frontend is written using React and Next.js. It provides a user interface to search for cultural assets and other entities

You can find the frontend code in the `frontend` folder.
Instructions to run the frontend can be found in the [README.md](frontend/README.md) in the `frontend` folder.

## Matching

The matching package contains code for the matching of cultural assets. The code is written in Python using PyTorch.
Instructions to run the matching code can be found in the [README.md](matching/README.md) file.

## ETL

The ETL package contains code to extract, transform and load data from the CSV files provided into the Neo4j database.
Instructions to run the ETL code can be found in the [README.md](etl/README.md) file.

## Ontology

The ontology package contains code to build the ontology we created for the project.
Instructions to run the ontology code can be found in the [README.md](ontology/README.md) file.

## Scraper

The scraper package contains all code relevant to scraping information from different websites for the project.
Instructions to run the scraper code can be found in the [README.md](scraper/README.md) file.

## Delab

The delab package contains utility functions for running jobs on the DE-Lab cluster.

## E2E-Tests

When developing e2e-tests using playwright, you should put them into the `e2e_tests` folder.
Instructions to run the code can be found in the [README.md](e2e_tests/README.md) file.

## Data

The raw data could not be made publicly available as part of the project repository. To add data sources for integration, use the `data` folder.
