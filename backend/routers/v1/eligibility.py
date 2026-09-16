"""
Eligibility assessment endpoints.

This module provides endpoints for patient eligibility assessment.
"""

import uuid

from fastapi import APIRouter, Depends

from backend.core.providers.base import LyzrProvider
from backend.dependencies.providers import get_lyzr_provider
from backend.schemas.eligibility import EligibilityRequest, EligibilityResponse

router = APIRouter()


@router.post("/eligibility/assess", response_model=EligibilityResponse)
async def assess_eligibility(
    request: EligibilityRequest,
    lyzr_provider: LyzrProvider = Depends(get_lyzr_provider),
) -> EligibilityResponse:
    """
    Assess patient eligibility for a clinical trial protocol.

    Args:
        request: Eligibility assessment request with patient and protocol data.
        lyzr_provider: Injected Lyzr provider instance.

    Returns:
        EligibilityResponse: Eligibility assessment result.
    """
    agent_id = await lyzr_provider.create_agent(
        agent_type="eligibility",
        config={"model_name": "eligibility-model"},
    )

    result = await lyzr_provider.execute_agent(
        agent_id=agent_id,
        input_data={
            "patient_id": request.patient_id,
            "protocol_id": request.protocol_id,
            "patient_data": request.patient_data,
            "protocol_data": request.protocol_data,
        },
    )

    return EligibilityResponse(
        assessment_id=str(uuid.uuid4()),
        patient_id=request.patient_id,
        protocol_id=request.protocol_id,
        is_eligible=result.get("eligible", False),
        confidence_score=result.get("confidence_score", 0.0),
        inclusion_evaluations=[],
        exclusion_evaluations=[],
        recommendation=result.get("recommendation", ""),
        rationale=result.get("recommendation", ""),
    )
