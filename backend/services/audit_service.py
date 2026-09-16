"""
Audit service.

This module provides business logic for regulatory audit generation.
"""

from backend.core.logging_config import get_logger
from backend.core.providers.base import LyzrProvider
from backend.dependencies.providers import get_lyzr_provider
from backend.schemas.audit import AuditReport, AuditRequest

logger = get_logger(__name__)


class AuditService:
    """
    Service for regulatory audit generation.
    """

    def __init__(self, lyzr_provider: LyzrProvider) -> None:
        """
        Initialize the audit service.

        Args:
            lyzr_provider: Lyzr provider instance.
        """
        self.lyzr_provider = lyzr_provider

    async def generate_audit(self, request: AuditRequest) -> AuditReport:
        """
        Generate a regulatory audit report for patient screening.

        Args:
            request: Audit request.

        Returns:
            AuditReport: Generated audit report.
        """
        logger.info(
            f"Generating audit for patient {request.patient_id} "
            f"against protocol {request.protocol_id}"
        )

        agent_id = await self.lyzr_provider.create_agent(
            agent_type="audit",
            config={"model_name": "audit-model"},
        )

        result = await self.lyzr_provider.execute_agent(
            agent_id=agent_id,
            input_data={
                "patient_id": request.patient_id,
                "protocol_id": request.protocol_id,
                "screening_data": request.screening_data,
                "eligibility_result": request.eligibility_result,
                "phi_redaction_data": request.phi_redaction_data,
            },
        )

        logger.info(
            f"Audit generation completed for patient {request.patient_id}: "
            f"Compliance={result.get('compliance_status', 'unknown')}"
        )

        return AuditReport(
            audit_id="AUDIT_" + request.patient_id,
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


def get_audit_service() -> AuditService:
    """
    Get the audit service instance.

    Returns:
        AuditService: Configured audit service.
    """
    return AuditService(get_lyzr_provider())
