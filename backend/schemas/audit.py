"""
Audit-related Pydantic schemas.

This module defines schemas for regulatory audit and compliance.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AuditFinding(BaseModel):
    """Individual audit finding."""

    category: str = Field(..., description="Finding category")
    severity: str = Field(..., description="Finding severity")
    description: str = Field(..., description="Finding description")
    status: str = Field(..., description="Finding status")
    recommendation: str | None = Field(None, description="Recommendation")


class ComplianceCheck(BaseModel):
    """Individual compliance check result."""

    check_name: str = Field(..., description="Name of compliance check")
    regulation: str = Field(..., description="Applicable regulation")
    status: str = Field(..., description="Compliance status")
    details: str = Field(..., description="Check details")


class AuditReport(BaseModel):
    """Complete audit report."""

    audit_id: str = Field(..., description="Audit identifier")
    patient_id: str = Field(..., description="Patient identifier")
    protocol_id: str = Field(..., description="Protocol identifier")
    audit_date: datetime = Field(default_factory=datetime.utcnow)
    auditor: str = Field(..., description="Auditor identifier")
    overall_compliance_status: str = Field(..., description="Overall compliance status")
    compliance_score: float = Field(..., ge=0.0, le=100.0, description="Compliance score")
    findings: list[AuditFinding] = Field(default_factory=list)
    compliance_checks: list[ComplianceCheck] = Field(default_factory=list)
    regulatory_references: list[str] = Field(default_factory=list)
    recommendations: str = Field(..., description="Overall recommendations")


class AuditRequest(BaseModel):
    """Schema for audit request."""

    patient_id: str = Field(..., description="Patient identifier")
    protocol_id: str = Field(..., description="Protocol identifier")
    screening_data: dict[str, Any] = Field(..., description="Screening process data")
    eligibility_result: dict[str, Any] = Field(..., description="Eligibility result")
    phi_redaction_data: dict[str, Any] = Field(..., description="PHI redaction data")


class AuditResponse(AuditReport):
    """Schema for audit response."""

    generated_at: datetime = Field(default_factory=datetime.utcnow)
