"""
Eligibility assessment service.

This module provides business logic for patient eligibility assessment.
"""


from backend.core.logging_config import get_logger
from backend.core.providers.base import LyzrProvider
from backend.dependencies.providers import get_lyzr_provider
from backend.schemas.eligibility import EligibilityRequest, EligibilityResult

logger = get_logger(__name__)


class EligibilityService:
    """
    Service for patient eligibility assessment.
    """

    def __init__(self, lyzr_provider: LyzrProvider) -> None:
        """
        Initialize the eligibility service.

        Args:
            lyzr_provider: Lyzr provider instance.
        """
        self.lyzr_provider = lyzr_provider

    async def assess_eligibility(self, request: EligibilityRequest) -> EligibilityResult:
        """
        Assess patient eligibility for a clinical trial protocol.

        Args:
            request: Eligibility assessment request.

        Returns:
            EligibilityResult: Eligibility assessment result.
        """
        logger.info(
            f"Assessing eligibility for patient {request.patient_id} "
            f"against protocol {request.protocol_id}"
        )

        agent_id = await self.lyzr_provider.create_agent(
            agent_type="eligibility",
            config={"model_name": "eligibility-model"},
        )

        result = await self.lyzr_provider.execute_agent(
            agent_id=agent_id,
            input_data={
                "patient_id": request.patient_id,
                "protocol_id": request.protocol_id,
                "patient_data": request.patient_data,
                "protocol_data": request.protocol_data,
            },
        )

        logger.info(
            f"Eligibility assessment completed for patient {request.patient_id}: "
            f"Eligible={result.get('eligible', False)}"
        )

        return EligibilityResult(
            patient_id=request.patient_id,
            protocol_id=request.protocol_id,
            is_eligible=result.get("eligible", False),
            confidence_score=result.get("confidence_score", 0.0),
            inclusion_evaluations=[],
            exclusion_evaluations=[],
            recommendation=result.get("recommendation", ""),
            rationale=result.get("recommendation", ""),
        )


def get_eligibility_service() -> EligibilityService:
    """
    Get the eligibility service instance.

    Returns:
        EligibilityService: Configured eligibility service.
    """
    return EligibilityService(get_lyzr_provider())
