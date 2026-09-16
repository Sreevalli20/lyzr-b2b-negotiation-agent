"""
Mock Lyzr provider for offline development.

This module provides a deterministic mock implementation of the Lyzr agent provider,
returning realistic agent responses without requiring external API keys.
"""

import hashlib
from typing import Any

from backend.core.providers.base import LyzrProvider


class MockLyzrProvider(LyzrProvider):
    """
    Mock Lyzr provider with deterministic responses.

    This provider simulates agent creation and execution with consistent responses,
    enabling offline development and testing without API keys.
    """

    def __init__(self) -> None:
        """Initialize the mock Lyzr provider."""
        self._agents: dict[str, dict[str, Any]] = {}
        self._agent_counter = 0

    async def create_agent(
        self,
        agent_type: str,
        config: dict[str, Any],
    ) -> str:
        """
        Create a mock agent instance.

        Args:
            agent_type: Type of agent to create.
            config: Agent configuration parameters.

        Returns:
            str: Mock agent ID.
        """
        self._agent_counter += 1
        agent_id = f"mock_agent_{agent_type}_{self._agent_counter}"

        self._agents[agent_id] = {
            "id": agent_id,
            "type": agent_type,
            "config": config,
            "status": "active",
            "created_at": "2024-01-15T00:00:00Z",
        }

        return agent_id

    async def execute_agent(
        self,
        agent_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute a mock agent with input data.

        Args:
            agent_id: ID of the agent to execute.
            input_data: Input data for the agent.

        Returns:
            dict: Mock agent execution result.
        """
        agent = self._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        agent_type = agent["type"]
        input_hash = hashlib.md5(str(input_data).encode()).hexdigest()

        return self._generate_execution_result(agent_type, input_data, input_hash)

    async def get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """
        Get the status of a mock agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            dict: Agent status information.
        """
        agent = self._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")

        return {
            "agent_id": agent["id"],
            "type": agent["type"],
            "status": agent["status"],
            "created_at": agent["created_at"],
            "last_execution": "2024-01-15T00:00:00Z",
        }

    def _generate_execution_result(
        self,
        agent_type: str,
        input_data: dict[str, Any],
        input_hash: str,
    ) -> dict[str, Any]:
        """
        Generate a deterministic execution result based on agent type.

        Args:
            agent_type: Type of agent being executed.
            input_data: Input data for the agent.
            input_hash: Hash for determinism.

        Returns:
            dict: Execution result.
        """
        if agent_type == "ingestion":
            return self._ingestion_result(input_data)
        elif agent_type == "protocol":
            return self._protocol_result(input_data)
        elif agent_type == "phi_scrubber":
            return self._phi_result(input_data)
        elif agent_type == "eligibility":
            return self._eligibility_result(input_data)
        elif agent_type == "medical_safety":
            return self._safety_result(input_data)
        elif agent_type == "audit":
            return self._audit_result(input_data)
        else:
            return self._generic_result(agent_type, input_data)

    def _ingestion_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock ingestion agent result."""
        return {
            "status": "success",
            "data_type": input_data.get("data_type", "unknown"),
            "records_processed": 1,
            "validation": {
                "passed": True,
                "errors": [],
                "warnings": [],
            },
            "extracted_fields": [
                "patient_id",
                "age",
                "diagnosis",
                "medications",
                "lab_results",
            ],
            "normalized_data": {
                "patient_id": "PATIENT_001",
                "age": 52,
                "diagnosis": "E11.9",
                "medications": ["Metformin", "Lisinopril"],
            },
        }

    def _protocol_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock protocol agent result."""
        return {
            "status": "success",
            "protocol_id": input_data.get("protocol_id", "PROTOCOL_001"),
            "criteria": {
                "inclusion": [
                    "Age 18-75",
                    "Type 2 Diabetes",
                    "HbA1c 7.0-10.0%",
                    "BMI 25-40",
                ],
                "exclusion": [
                    "Type 1 Diabetes",
                    "Severe renal impairment",
                    "Active cardiovascular disease",
                    "Pregnancy",
                ],
            },
            "study_details": {
                "duration_weeks": 24,
                "visits_required": 8,
                "primary_endpoint": "HbA1c change",
            },
        }

    def _phi_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock PHI scrubber result."""
        return {
            "status": "success",
            "phi_detected": 6,
            "phi_redacted": 6,
            "redacted_fields": [
                "patient_name",
                "date_of_birth",
                "ssn",
                "address",
                "phone",
                "email",
            ],
            "compliance": "HIPAA/GDPR compliant",
            "redacted_data": input_data.get("data", {}),
        }

    def _eligibility_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock eligibility agent result."""
        return {
            "status": "success",
            "eligible": True,
            "confidence_score": 0.94,
            "criteria_met": {
                "age": True,
                "diagnosis": True,
                "hba1c": True,
                "bmi": True,
                "medication_stable": True,
            },
            "exclusion_checks": {
                "type1_diabetes": False,
                "renal_impairment": False,
                "cardiovascular_disease": False,
                "pregnancy": False,
            },
            "recommendation": "Proceed with screening",
        }

    def _safety_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock medical safety agent result."""
        return {
            "status": "success",
            "safety_status": "safe_to_proceed",
            "risk_factors": ["mild_hypertension"],
            "drug_interactions": [],
            "lab_safety": {
                "liver_function": "normal",
                "kidney_function": "mild_impairment_acceptable",
                "blood_counts": "normal",
            },
            "clearance": "approved",
            "monitoring_recommendations": [
                "weekly_glucose",
                "monthly_renal",
                "visit_bp",
            ],
        }

    def _audit_result(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate mock audit agent result."""
        return {
            "status": "success",
            "compliance_status": "compliant",
            "audit_date": "2024-01-15",
            "findings": {
                "protocol_adherence": 100,
                "phi_protection": "fully_compliant",
                "eligibility_criteria": "properly_applied",
                "documentation": "complete",
            },
            "regulatory_references": [
                "21 CFR Part 312",
                "ICH-GCP E6",
                "HIPAA Privacy Rule",
            ],
            "recommendations": "continue_current_procedures",
            "audit_trail_id": "AUDIT_2024_001",
        }

    def _generic_result(self, agent_type: str, input_data: dict[str, Any]) -> dict[str, Any]:
        """Generate a generic mock result."""
        return {
            "status": "success",
            "agent_type": agent_type,
            "input_received": True,
            "result": f"Mock execution for {agent_type}",
        }
