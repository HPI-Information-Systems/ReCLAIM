FROM python:3.12.2
WORKDIR /fastapi
COPY ./pyproject.toml /fastapi/pyproject.toml
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN ~/.local/bin/poetry install
COPY ./backend /fastapi/backend
COPY ./combined_schema.ttl /fastapi/combined_schema.ttl
ENV SCHEMA_FILE_PATH="/fastapi/combined_schema.ttl"
CMD ["/root/.local/bin/poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
