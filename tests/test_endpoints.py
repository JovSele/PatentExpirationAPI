"""
Basic tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["status"] == "operational"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database" in data


def test_legal_disclaimer():
    """Test legal disclaimer endpoint."""
    response = client.get("/disclaimer")
    assert response.status_code == 200
    data = response.json()
    assert "disclaimer" in data
    assert "NO WARRANTY" in data["disclaimer"]


def test_patent_status_invalid_format():
    """Test patent status with invalid format."""
    response = client.get("/api/v1/status?patent=INVALID123")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data["detail"]


def test_patent_status_missing_patent():
    """Test patent status without patent parameter."""
    response = client.get("/api/v1/status")
    assert response.status_code == 422  # FastAPI validation error


# Mock tests (will need actual API keys for integration tests)
@pytest.mark.skip(reason="Requires API keys and external services")
def test_patent_status_epo():
    """Test EPO patent lookup (requires API keys)."""
    response = client.get("/api/v1/status?patent=EP1234567")
    assert response.status_code in [200, 404, 500]
    # Cannot test actual response without valid patent and API keys


@pytest.mark.skip(reason="Requires API keys and external services")
def test_patent_status_uspto():
    """Test USPTO patent lookup (requires API keys)."""
    response = client.get("/api/v1/status?patent=US7654321")
    assert response.status_code in [200, 404, 500]
    # Cannot test actual response without valid patent and API keys
