"""
Protocol-related Pydantic schemas.

This module defines schemas for clinical trial protocols.
"""

from datetime import date

from pydantic import BaseModel, Field


class InclusionCriteria(BaseModel):
    """Inclusion criteria for trial participation."""

    criterion_id: str = Field(..., description="Criterion identifier")
    description: str = Field(..., description="Criterion description")
    category: str = Field(..., description="Criterion category")
    required: bool = Field(default=True, description="Required or optional")


class ExclusionCriteria(BaseModel):
    """Exclusion criteria for trial participation."""

    criterion_id: str = Field(..., description="Criterion identifier")
    description: str = Field(..., description="Criterion description")
    category: str = Field(..., description="Criterion category")
    severity: str = Field(..., description="Severity level if violated")


class StudyTimeline(BaseModel):
    """Study timeline and visit schedule."""

    total_duration_weeks: int = Field(..., ge=1, description="Total study duration")
    total_visits: int = Field(..., ge=1, description="Total number of visits")
    visit_frequency: str = Field(..., description="Visit frequency pattern")
    screening_period_weeks: int = Field(..., ge=0, description="Screening period")
    treatment_period_weeks: int = Field(..., ge=0, description="Treatment period")
    follow_up_period_weeks: int = Field(..., ge=0, description="Follow-up period")


class StudyEndpoints(BaseModel):
    """Primary and secondary study endpoints."""

    primary_endpoint: str = Field(..., description="Primary endpoint description")
    secondary_endpoints: list[str] = Field(default_factory=list)
    exploratory_endpoints: list[str] = Field(default_factory=list)


class SafetyRequirements(BaseModel):
    """Safety monitoring requirements."""

    required_lab_tests: list[str] = Field(default_factory=list)
    monitoring_frequency: str = Field(..., description="Safety monitoring frequency")
    stopping_rules: list[str] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)


class ClinicalProtocol(BaseModel):
    """Complete clinical trial protocol."""

    protocol_id: str = Field(..., description="Protocol identifier")
    protocol_number: str = Field(..., description="Protocol number")
    title: str = Field(..., description="Protocol title")
    phase: str = Field(..., description="Trial phase")
    therapeutic_area: str = Field(..., description="Therapeutic area")
    inclusion_criteria: list[InclusionCriteria] = Field(default_factory=list)
    exclusion_criteria: list[ExclusionCriteria] = Field(default_factory=list)
    timeline: StudyTimeline
    endpoints: StudyEndpoints
    safety_requirements: SafetyRequirements
    target_enrollment: int = Field(..., ge=1, description="Target enrollment")
    sponsor: str = Field(..., description="Trial sponsor")
    version: str = Field(..., description="Protocol version")
    effective_date: date = Field(..., description="Protocol effective date")


class ProtocolCreate(BaseModel):
    """Schema for creating a new protocol."""

    protocol_id: str = Field(..., description="Protocol identifier")
    protocol_number: str = Field(..., description="Protocol number")
    title: str = Field(..., description="Protocol title")
    phase: str = Field(..., description="Trial phase")
    therapeutic_area: str = Field(..., description="Therapeutic area")
    inclusion_criteria: list[InclusionCriteria] = Field(default_factory=list)
    exclusion_criteria: list[ExclusionCriteria] = Field(default_factory=list)
    timeline: StudyTimeline
    endpoints: StudyEndpoints
    safety_requirements: SafetyRequirements
    target_enrollment: int = Field(..., ge=1, description="Target enrollment")
    sponsor: str = Field(..., description="Trial sponsor")
    version: str = Field(..., description="Protocol version")
    effective_date: date = Field(..., description="Protocol effective date")


class ProtocolResponse(ClinicalProtocol):
    """Schema for protocol response."""

    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
