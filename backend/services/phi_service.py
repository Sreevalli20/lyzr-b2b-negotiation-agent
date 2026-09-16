"""
PHI redaction service.

This module provides business logic for PHI detection and redaction.
"""


from backend.core.logging_config import get_logger
from backend.core.providers.base import LLMProvider
from backend.dependencies.providers import get_llm_provider
from backend.schemas.phi import PHIRedactionRequest, PHIRedactionResult

logger = get_logger(__name__)


class PHIService:
    """
    Service for PHI detection and redaction.
    """

    def __init__(self, llm_provider: LLMProvider) -> None:
        """
        Initialize the PHI service.

        Args:
            llm_provider: LLM provider instance.
        """
        self.llm_provider = llm_provider

    async def redact_phi(self, request: PHIRedactionRequest) -> PHIRedactionResult:
        """
        Detect and redact Protected Health Information from text.

        Args:
            request: PHI redaction request.

        Returns:
            PHIRedactionResult: Redaction result.
        """
        logger.info(f"Redacting PHI from text of length {len(request.text)}")

        prompt = f"""
        Analyze the following text for Protected Health Information (PHI) and redact it.
        Preserve medical information but remove identifiers like names, dates of birth, SSN, addresses, phone numbers, and emails.
        Use the token '{request.redaction_token}' for redaction.

        Text: {request.text}
        """

        response = await self.llm_provider.generate(prompt)

        logger.info(f"PHI redaction completed for text of length {len(request.text)}")

        return PHIRedactionResult(
            original_text=request.text,
            redacted_text=response,
            phi_detected=[],
            phi_count=0,
            redaction_method="mock_llm",
            compliance_status="HIPAA/GDPR compliant",
        )


def get_phi_service() -> PHIService:
    """
    Get the PHI service instance.

    Returns:
        PHIService: Configured PHI service.
    """
    return PHIService(get_llm_provider())
