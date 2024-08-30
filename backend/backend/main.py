"""
    Main module for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import (
    autocomplete,
    cultural_asset,
    collection,
    person,
    health,
)

app = FastAPI()

routers = [
    health.router,
    cultural_asset.router,
    person.router,
    collection.router,
    autocomplete.router,
]

for router in routers:
    app.include_router(router)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://http://vm-bp2024fn1.cloud.dhclab.i.hpi.de:3000",
        "https://kunstgraph.dhc-lab.hpi.de",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """
    Simple custom OpenAPI schema.
    """

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Kunstgraph API",
        version="0.0.1",
        description="This is the API for the Kunstgraph - the platform developed during the HPI-JDCRP Bachelorproject in 2023/24.",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_schema = custom_openapi()
