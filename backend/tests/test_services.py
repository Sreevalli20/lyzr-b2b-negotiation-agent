"""
Tests for service layer.

This module contains tests for business logic services.
"""

import pytest

from backend.core.providers.mock_llm import MockLLMProvider
from backend.core.providers.mock_lyzr import MockLyzrProvider
from backend.schemas.audit import AuditRequest
from backend.schemas.eligibility import EligibilityRequest
from backend.schemas.phi import PHIRedactionRequest
from backend.services.audit_service import AuditService
from backend.services.eligibility_service import EligibilityService
from backend.services.phi_service import PHIService


@pytest.mark.asyncio
class TestEligibilityService:
    """Test suite for EligibilityService."""

    @pytest.fixture
    def service(self) -> EligibilityService:
        """Fixture for EligibilityService instance."""
        return EligibilityService(MockLyzrProvider())

    async def test_assess_eligibility(self, service: EligibilityService) -> None:
        """Test eligibility assessment."""
        request = EligibilityRequest(
            patient_id="PATIENT_001",
            protocol_id="PROTOCOL_001",
            patient_data={},
            protocol_data={},
        )
        result = await service.assess_eligibility(request)
        assert result.patient_id == "PATIENT_001"
        assert result.protocol_id == "PROTOCOL_001"
        assert isinstance(result.is_eligible, bool)
        assert 0.0 <= result.confidence_score <= 1.0


@pytest.mark.asyncio
class TestPHIService:
    """Test suite for PHIService."""

    @pytest.fixture
    def service(self) -> PHIService:
        """Fixture for PHIService instance."""
        return PHIService(MockLLMProvider())

    async def test_redact_phi(self, service: PHIService) -> None:
        """Test PHI redaction."""
        request = PHIRedactionRequest(
            text="Patient name: John Doe",
            preserve_medical_info=True,
            redaction_token="[REDACTED]",
        )
        result = await service.redact_phi(request)
        assert result.original_text == "Patient name: John Doe"
        assert isinstance(result.redacted_text, str)
        assert result.compliance_status == "HIPAA/GDPR compliant"


@pytest.mark.asyncio
class TestAuditService:
    """Test suite for AuditService."""

    @pytest.fixture
    def service(self) -> AuditService:
        """Fixture for AuditService instance."""
        return AuditService(MockLyzrProvider())

    async def test_generate_audit(self, service: AuditService) -> None:
        """Test audit generation."""
        request = AuditRequest(
            patient_id="PATIENT_001",
            protocol_id="PROTOCOL_001",
            screening_data={},
            eligibility_result={},
            phi_redaction_data={},
        )
        result = await service.generate_audit(request)
        assert result.patient_id == "PATIENT_001"
        assert result.protocol_id == "PROTOCOL_001"
        assert result.overall_compliance_status in ["compliant", "non_compliant"]
        assert 0.0 <= result.compliance_score <= 100.0
