"""
Eligibility-related Pydantic schemas.

This module defines schemas for patient eligibility assessment.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CriterionEvaluation(BaseModel):
    """Evaluation of a single criterion."""

    criterion_id: str = Field(..., description="Criterion identifier")
    criterion_type: str = Field(..., description="Inclusion or exclusion")
    description: str = Field(..., description="Criterion description")
    met: bool = Field(..., description="Whether criterion is met")
    evidence: str = Field(..., description="Evidence for decision")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class EligibilityResult(BaseModel):
    """Complete eligibility assessment result."""

    patient_id: str = Field(..., description="Patient identifier")
    protocol_id: str = Field(..., description="Protocol identifier")
    is_eligible: bool = Field(..., description="Overall eligibility status")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    inclusion_evaluations: list[CriterionEvaluation] = Field(default_factory=list)
    exclusion_evaluations: list[CriterionEvaluation] = Field(default_factory=list)
    recommendation: str = Field(..., description="Eligibility recommendation")
    rationale: str = Field(..., description="Detailed rationale")
    assessed_at: datetime = Field(default_factory=datetime.utcnow)


class EligibilityRequest(BaseModel):
    """Schema for eligibility assessment request."""

    patient_id: str = Field(..., description="Patient identifier")
    protocol_id: str = Field(..., description="Protocol identifier")
    patient_data: dict[str, Any] = Field(..., description="Patient EHR data")
    protocol_data: dict[str, Any] = Field(..., description="Protocol data")


class EligibilityResponse(EligibilityResult):
    """Schema for eligibility assessment response."""

    assessment_id: str = Field(..., description="Assessment identifier")
