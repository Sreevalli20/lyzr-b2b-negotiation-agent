"""
Tests for Pydantic schemas.

This module contains tests for all schema validation.
"""

from datetime import date

from backend.schemas.agent import AgentConfig, AgentExecutionRequest
from backend.schemas.audit import AuditReport, AuditRequest
from backend.schemas.eligibility import EligibilityRequest, EligibilityResult
from backend.schemas.patient import (
    LabResult,
    MedicalCondition,
    Medication,
    PatientDemographics,
    PatientEHR,
)
from backend.schemas.phi import PHIRedactionRequest, PHIRedactionResult
from backend.schemas.protocol import (
    ClinicalProtocol,
    InclusionCriteria,
    StudyTimeline,
)


class TestPatientSchemas:
    """Test suite for patient-related schemas."""

    def test_patient_demographics(self) -> None:
        """Test PatientDemographics schema."""
        data = {
            "patient_id": "PATIENT_001",
            "age": 52,
            "age_group": "45-54",
            "gender": "Female",
        }
        demographics = PatientDemographics(**data)
        assert demographics.patient_id == "PATIENT_001"
        assert demographics.age == 52

    def test_medical_condition(self) -> None:
        """Test MedicalCondition schema."""
        data = {
            "code": "E11.9",
            "description": "Type 2 Diabetes",
            "severity": "moderate",
        }
        condition = MedicalCondition(**data)
        assert condition.code == "E11.9"

    def test_medication(self) -> None:
        """Test Medication schema."""
        data = {
            "name": "Metformin",
            "dosage": "1000 mg",
            "frequency": "Twice daily",
            "start_date": date(2024, 1, 1),
        }
        medication = Medication(**data)
        assert medication.name == "Metformin"

    def test_lab_result(self) -> None:
        """Test LabResult schema."""
        data = {
            "test_name": "HbA1c",
            "test_code": "4548-4",
            "value": "8.2",
            "unit": "%",
            "reference_range": "4.0-5.6",
            "test_date": date(2024, 1, 10),
        }
        result = LabResult(**data)
        assert result.test_name == "HbA1c"

    def test_patient_ehr(self) -> None:
        """Test PatientEHR schema."""
        data = {
            "demographics": {
                "patient_id": "PATIENT_001",
                "age": 52,
                "age_group": "45-54",
                "gender": "Female",
            },
            "conditions": [],
            "medications": [],
            "lab_results": [],
            "vital_signs": [],
        }
        ehr = PatientEHR(**data)
        assert ehr.demographics.patient_id == "PATIENT_001"


class TestProtocolSchemas:
    """Test suite for protocol-related schemas."""

    def test_inclusion_criteria(self) -> None:
        """Test InclusionCriteria schema."""
        data = {
            "criterion_id": "INC_001",
            "description": "Age 18-75",
            "category": "Demographics",
        }
        criteria = InclusionCriteria(**data)
        assert criteria.criterion_id == "INC_001"

    def test_study_timeline(self) -> None:
        """Test StudyTimeline schema."""
        data = {
            "total_duration_weeks": 24,
            "total_visits": 8,
            "visit_frequency": "Every 3-4 weeks",
            "screening_period_weeks": 4,
            "treatment_period_weeks": 24,
            "follow_up_period_weeks": 4,
        }
        timeline = StudyTimeline(**data)
        assert timeline.total_duration_weeks == 24

    def test_clinical_protocol(self) -> None:
        """Test ClinicalProtocol schema."""
        data = {
            "protocol_id": "PROTOCOL_001",
            "protocol_number": "DIAB-2024-001",
            "title": "Diabetes Study",
            "phase": "Phase 3",
            "therapeutic_area": "Endocrinology",
            "inclusion_criteria": [],
            "exclusion_criteria": [],
            "timeline": {
                "total_duration_weeks": 24,
                "total_visits": 8,
                "visit_frequency": "Every 3-4 weeks",
                "screening_period_weeks": 4,
                "treatment_period_weeks": 24,
                "follow_up_period_weeks": 4,
            },
            "endpoints": {
                "primary_endpoint": "HbA1c change",
                "secondary_endpoints": [],
                "exploratory_endpoints": [],
            },
            "safety_requirements": {
                "required_lab_tests": [],
                "monitoring_frequency": "Every visit",
                "stopping_rules": [],
                "contraindications": [],
            },
            "target_enrollment": 500,
            "sponsor": "PharmaCorp",
            "version": "1.0",
            "effective_date": date(2024, 1, 1),
        }
        protocol = ClinicalProtocol(**data)
        assert protocol.protocol_id == "PROTOCOL_001"


class TestEligibilitySchemas:
    """Test suite for eligibility schemas."""

    def test_eligibility_request(self) -> None:
        """Test EligibilityRequest schema."""
        data = {
            "patient_id": "PATIENT_001",
            "protocol_id": "PROTOCOL_001",
            "patient_data": {},
            "protocol_data": {},
        }
        request = EligibilityRequest(**data)
        assert request.patient_id == "PATIENT_001"

    def test_eligibility_result(self) -> None:
        """Test EligibilityResult schema."""
        data = {
            "patient_id": "PATIENT_001",
            "protocol_id": "PROTOCOL_001",
            "is_eligible": True,
            "confidence_score": 0.94,
            "recommendation": "Proceed",
            "rationale": "Meets all criteria",
        }
        result = EligibilityResult(**data)
        assert result.is_eligible is True
        assert result.confidence_score == 0.94


class TestPHISchemas:
    """Test suite for PHI schemas."""

    def test_phi_redaction_request(self) -> None:
        """Test PHIRedactionRequest schema."""
        data = {
            "text": "Patient name: John Doe",
            "preserve_medical_info": True,
            "redaction_token": "[REDACTED]",
        }
        request = PHIRedactionRequest(**data)
        assert request.text == "Patient name: John Doe"

    def test_phi_redaction_result(self) -> None:
        """Test PHIRedactionResult schema."""
        data = {
            "original_text": "Patient name: John Doe",
            "redacted_text": "Patient name: [REDACTED]",
            "phi_detected": [],
            "phi_count": 1,
            "redaction_method": "mock",
            "compliance_status": "compliant",
        }
        result = PHIRedactionResult(**data)
        assert result.phi_count == 1


class TestAuditSchemas:
    """Test suite for audit schemas."""

    def test_audit_request(self) -> None:
        """Test AuditRequest schema."""
        data = {
            "patient_id": "PATIENT_001",
            "protocol_id": "PROTOCOL_001",
            "screening_data": {},
            "eligibility_result": {},
            "phi_redaction_data": {},
        }
        request = AuditRequest(**data)
        assert request.patient_id == "PATIENT_001"

    def test_audit_report(self) -> None:
        """Test AuditReport schema."""
        data = {
            "audit_id": "AUDIT_001",
            "patient_id": "PATIENT_001",
            "protocol_id": "PROTOCOL_001",
            "auditor": "System",
            "overall_compliance_status": "compliant",
            "compliance_score": 100,
            "findings": [],
            "compliance_checks": [],
            "regulatory_references": [],
            "recommendations": "Continue",
        }
        report = AuditReport(**data)
        assert report.compliance_score == 100


class TestAgentSchemas:
    """Test suite for agent schemas."""

    def test_agent_config(self) -> None:
        """Test AgentConfig schema."""
        data = {
            "agent_type": "eligibility",
            "model_name": "model-v1",
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        config = AgentConfig(**data)
        assert config.agent_type == "eligibility"

    def test_agent_execution_request(self) -> None:
        """Test AgentExecutionRequest schema."""
        data = {
            "agent_type": "eligibility",
            "input_data": {"patient_id": "123"},
        }
        request = AgentExecutionRequest(**data)
        assert request.agent_type == "eligibility"
