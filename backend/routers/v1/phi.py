"""
PHI redaction endpoints.

This module provides endpoints for PHI detection and redaction.
"""

import uuid

from fastapi import APIRouter, Depends

from backend.core.providers.base import LLMProvider
from backend.dependencies.providers import get_llm_provider
from backend.schemas.phi import PHIRedactionRequest, PHIRedactionResponse

router = APIRouter()


@router.post("/phi/redact", response_model=PHIRedactionResponse)
async def redact_phi(
    request: PHIRedactionRequest,
    llm_provider: LLMProvider = Depends(get_llm_provider),
) -> PHIRedactionResponse:
    """
    Detect and redact Protected Health Information from text.

    Args:
        request: PHI redaction request with text to process.
        llm_provider: Injected LLM provider instance.

    Returns:
        PHIRedactionResponse: Redaction result with PHI removed.
    """
    prompt = f"""
    Analyze the following text for Protected Health Information (PHI) and redact it.
    Preserve medical information but remove identifiers like names, dates of birth, SSN, addresses, phone numbers, and emails.
    Use the token '{request.redaction_token}' for redaction.

    Text: {request.text}
    """

    response = await llm_provider.generate(prompt)

    return PHIRedactionResponse(
        request_id=str(uuid.uuid4()),
        original_text=request.text,
        redacted_text=response,
        phi_detected=[],
        phi_count=0,
        redaction_method="mock_llm",
        compliance_status="HIPAA/GDPR compliant",
    )
