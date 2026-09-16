"""
PHI-related Pydantic schemas.

This module defines schemas for PHI detection and redaction.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class PHIDetection(BaseModel):
    """Detected PHI entity."""

    entity_type: str = Field(..., description="Type of PHI (e.g., NAME, DOB, SSN)")
    text: str = Field(..., description="Original text containing PHI")
    start_position: int = Field(..., ge=0, description="Start position in text")
    end_position: int = Field(..., ge=0, description="End position in text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")


class PHIRedactionResult(BaseModel):
    """Result of PHI redaction process."""

    original_text: str = Field(..., description="Original text with PHI")
    redacted_text: str = Field(..., description="Redacted text")
    phi_detected: list[PHIDetection] = Field(default_factory=list)
    phi_count: int = Field(..., ge=0, description="Total PHI entities detected")
    redaction_method: str = Field(..., description="Redaction method used")
    compliance_status: str = Field(..., description="Compliance status")
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class PHIRedactionRequest(BaseModel):
    """Schema for PHI redaction request."""

    text: str = Field(..., description="Text to be redacted")
    preserve_medical_info: bool = Field(default=True, description="Preserve medical information")
    redaction_token: str = Field(default="[REDACTED]", description="Redaction token")


class PHIRedactionResponse(PHIRedactionResult):
    """Schema for PHI redaction response."""

    request_id: str = Field(..., description="Request identifier")
