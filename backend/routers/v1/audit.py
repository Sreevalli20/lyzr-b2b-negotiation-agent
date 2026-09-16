"""
Audit endpoints.

This module provides endpoints for regulatory audit and compliance.
"""

import uuid

from fastapi import APIRouter, Depends

from backend.core.providers.base import LyzrProvider
from backend.dependencies.providers import get_lyzr_provider
from backend.schemas.audit import AuditRequest, AuditResponse

router = APIRouter()


@router.post("/audit/generate", response_model=AuditResponse)
async def generate_audit(
    request: AuditRequest,
    lyzr_provider: LyzrProvider = Depends(get_lyzr_provider),
) -> AuditResponse:
    """
    Generate a regulatory audit report for patient screening.

    Args:
        request: Audit request with screening and eligibility data.
        lyzr_provider: Injected Lyzr provider instance.

    Returns:
        AuditResponse: Generated audit report.
    """
    agent_id = await lyzr_provider.create_agent(
        agent_type="audit",
        config={"model_name": "audit-model"},
    )

    result = await lyzr_provider.execute_agent(
        agent_id=agent_id,
        input_data={
            "patient_id": request.patient_id,
            "protocol_id": request.protocol_id,
            "screening_data": request.screening_data,
            "eligibility_result": request.eligibility_result,
            "phi_redaction_data": request.phi_redaction_data,
        },
    )

    return AuditResponse(
        audit_id=str(uuid.uuid4()),
        patient_id=request.patient_id,
        protocol_id=request.protocol_id,
        auditor="System Automated Audit",
        overall_compliance_status=result.get("compliance_status", "unknown"),
        compliance_score=result.get("findings", {}).get("protocol_adherence", 100),
        findings=[],
        compliance_checks=[],
        regulatory_references=result.get("regulatory_references", []),
        recommendations=result.get("recommendations", ""),
    )
