"""
Schemas module for Pydantic models.

This module exports all schema definitions.
"""

from backend.schemas.agent import (
    AgentConfig,
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentStatus,
)
from backend.schemas.audit import (
    AuditFinding,
    AuditReport,
    AuditRequest,
    AuditResponse,
    ComplianceCheck,
)
from backend.schemas.common import (
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
    PaginationParams,
    SuccessResponse,
)
from backend.schemas.eligibility import (
    CriterionEvaluation,
    EligibilityRequest,
    EligibilityResponse,
    EligibilityResult,
)
from backend.schemas.patient import (
    LabResult,
    MedicalCondition,
    Medication,
    PatientDemographics,
    PatientEHR,
    PatientEHRCreate,
    PatientEHRResponse,
    VitalSign,
)
from backend.schemas.phi import (
    PHIDetection,
    PHIRedactionRequest,
    PHIRedactionResponse,
    PHIRedactionResult,
)
from backend.schemas.protocol import (
    ClinicalProtocol,
    ExclusionCriteria,
    InclusionCriteria,
    ProtocolCreate,
    ProtocolResponse,
    SafetyRequirements,
    StudyEndpoints,
    StudyTimeline,
)

__all__ = [
    # Patient schemas
    "PatientDemographics",
    "MedicalCondition",
    "Medication",
    "LabResult",
    "VitalSign",
    "PatientEHR",
    "PatientEHRCreate",
    "PatientEHRResponse",
    # Protocol schemas
    "InclusionCriteria",
    "ExclusionCriteria",
    "StudyTimeline",
    "StudyEndpoints",
    "SafetyRequirements",
    "ClinicalProtocol",
    "ProtocolCreate",
    "ProtocolResponse",
    # Eligibility schemas
    "CriterionEvaluation",
    "EligibilityResult",
    "EligibilityRequest",
    "EligibilityResponse",
    # PHI schemas
    "PHIDetection",
    "PHIRedactionResult",
    "PHIRedactionRequest",
    "PHIRedactionResponse",
    # Audit schemas
    "AuditFinding",
    "ComplianceCheck",
    "AuditReport",
    "AuditRequest",
    "AuditResponse",
    # Agent schemas
    "AgentConfig",
    "AgentExecutionRequest",
    "AgentExecutionResult",
    "AgentStatus",
    # Common schemas
    "HealthResponse",
    "ErrorResponse",
    "SuccessResponse",
    "PaginationParams",
    "PaginatedResponse",
]
