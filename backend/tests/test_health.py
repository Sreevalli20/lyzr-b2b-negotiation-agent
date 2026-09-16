"""
Health endpoint tests.

This module contains tests for the health check endpoint.
"""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """
    Test the root endpoint returns correct project information.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "Governed Clinical Trial Patient Screening & Regulatory Audit Agent"
    assert data["status"] == "Production-ready offline foundation"
    assert data["competition"] == "HiDevs AI Quest 2026"


def test_health_endpoint() -> None:
    """
    Test the health endpoint returns healthy status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
