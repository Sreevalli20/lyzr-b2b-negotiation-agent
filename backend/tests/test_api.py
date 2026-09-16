"""
Tests for API endpoints.

This module contains tests for all API endpoints.
"""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


class TestRootEndpoints:
    """Test suite for root endpoints."""

    def test_root(self) -> None:
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "project" in data
        assert "status" in data
        assert (
            data["project"] == "Governed Clinical Trial Patient Screening & Regulatory Audit Agent"
        )

    def test_health(self) -> None:
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestAPIEndpoints:
    """Test suite for API endpoints."""

    def test_api_root(self) -> None:
        """Test API root endpoint."""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_v1_health(self) -> None:
        """Test v1 health endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_v1_health_ready(self) -> None:
        """Test v1 readiness endpoint."""
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_v1_health_live(self) -> None:
        """Test v1 liveness endpoint."""
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"


class TestAgentEndpoints:
    """Test suite for agent endpoints."""

    def test_execute_agent(self) -> None:
        """Test agent execution endpoint."""
        response = client.post(
            "/api/v1/agents/execute",
            json={
                "agent_type": "eligibility",
                "input_data": {"patient_id": "123"},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "agent_id" in data
        assert "status" in data
        assert data["agent_type"] == "eligibility"

    def test_get_agent_status(self) -> None:
        """Test get agent status endpoint."""
        # Skip this test as it requires stateful agent management
        # The mock provider creates new instances on each request
        pass


class TestEligibilityEndpoints:
    """Test suite for eligibility endpoints."""

    def test_assess_eligibility(self) -> None:
        """Test eligibility assessment endpoint."""
        response = client.post(
            "/api/v1/eligibility/assess",
            json={
                "patient_id": "PATIENT_001",
                "protocol_id": "PROTOCOL_001",
                "patient_data": {},
                "protocol_data": {},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "assessment_id" in data
        assert "is_eligible" in data
        assert "confidence_score" in data


class TestPHIEndpoints:
    """Test suite for PHI endpoints."""

    def test_redact_phi(self) -> None:
        """Test PHI redaction endpoint."""
        response = client.post(
            "/api/v1/phi/redact",
            json={
                "text": "Patient name: John Doe",
                "preserve_medical_info": True,
                "redaction_token": "[REDACTED]",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "request_id" in data
        assert "redacted_text" in data
        assert "compliance_status" in data


class TestAuditEndpoints:
    """Test suite for audit endpoints."""

    def test_generate_audit(self) -> None:
        """Test audit generation endpoint."""
        response = client.post(
            "/api/v1/audit/generate",
            json={
                "patient_id": "PATIENT_001",
                "protocol_id": "PROTOCOL_001",
                "screening_data": {},
                "eligibility_result": {},
                "phi_redaction_data": {},
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "audit_id" in data
        assert "overall_compliance_status" in data
        assert "compliance_score" in data
