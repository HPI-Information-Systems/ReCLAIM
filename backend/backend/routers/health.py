"""
Health check endpoint for the API. Returns a 200 status code if the API is up and running.
"""

from fastapi import APIRouter, Depends, status
from neo4j import Session

from ..dependencies.db import with_db


router = APIRouter(prefix="/health")


@router.get("/", status_code=status.HTTP_200_OK)
def health(session: Session = Depends(with_db)):
    """
    Simple health check for the API. Returns a 200 status code if the API is up and running.
    """
    
    session.run("MATCH (n) RETURN n LIMIT 1")

    return {"status": "ok"}
