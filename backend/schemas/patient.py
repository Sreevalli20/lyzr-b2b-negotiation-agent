"""
Patient-related Pydantic schemas.

This module defines schemas for patient data and medical records.
"""

from datetime import date

from pydantic import BaseModel, Field


class PatientDemographics(BaseModel):
    """Patient demographic information."""

    patient_id: str = Field(..., description="Unique patient identifier")
    age: int = Field(..., ge=0, le=150, description="Patient age")
    age_group: str = Field(..., description="Age group category")
    gender: str = Field(..., description="Patient gender")
    ethnicity: str | None = Field(None, description="Patient ethnicity")


class MedicalCondition(BaseModel):
    """Medical condition or diagnosis."""

    code: str = Field(..., description="ICD-10 or SNOMED code")
    description: str = Field(..., description="Condition description")
    severity: str = Field(..., description="Condition severity")
    onset_date: date | None = Field(None, description="Condition onset date")


class Medication(BaseModel):
    """Medication information."""

    name: str = Field(..., description="Medication name")
    dosage: str = Field(..., description="Dosage information")
    frequency: str = Field(..., description="Administration frequency")
    start_date: date = Field(..., description="Medication start date")
    is_stable: bool = Field(default=False, description="Medication stability status")


class LabResult(BaseModel):
    """Laboratory test result."""

    test_name: str = Field(..., description="Test name")
    test_code: str = Field(..., description="LOINC code")
    value: str = Field(..., description="Test result value")
    unit: str = Field(..., description="Unit of measurement")
    reference_range: str = Field(..., description="Normal reference range")
    is_abnormal: bool = Field(default=False, description="Abnormal result flag")
    test_date: date = Field(..., description="Test date")


class VitalSign(BaseModel):
    """Vital sign measurement."""

    name: str = Field(..., description="Vital sign name")
    value: float = Field(..., description="Measured value")
    unit: str = Field(..., description="Unit of measurement")
    recorded_date: date = Field(..., description="Recording date")


class PatientEHR(BaseModel):
    """Complete Electronic Health Record."""

    demographics: PatientDemographics
    conditions: list[MedicalCondition] = Field(default_factory=list)
    medications: list[Medication] = Field(default_factory=list)
    lab_results: list[LabResult] = Field(default_factory=list)
    vital_signs: list[VitalSign] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    medical_history: list[str] = Field(default_factory=list)


class PatientEHRCreate(BaseModel):
    """Schema for creating a new patient EHR."""

    demographics: PatientDemographics
    conditions: list[MedicalCondition] = Field(default_factory=list)
    medications: list[Medication] = Field(default_factory=list)
    lab_results: list[LabResult] = Field(default_factory=list)
    vital_signs: list[VitalSign] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    medical_history: list[str] = Field(default_factory=list)


class PatientEHRResponse(PatientEHR):
    """Schema for patient EHR response."""

    id: str = Field(..., description="EHR record ID")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
