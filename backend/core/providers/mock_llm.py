"""
Mock LLM provider for offline development.

This module provides a deterministic mock implementation of the LLM provider,
returning realistic responses without requiring external API keys.
"""

import hashlib
from typing import Any

from backend.core.providers.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    Mock LLM provider with deterministic responses.

    This provider generates consistent responses based on input hash,
    enabling offline development and testing without API keys.
    """

    def __init__(self) -> None:
        """Initialize the mock LLM provider."""
        self._response_cache: dict[str, str] = {}

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a deterministic mock response.

        Args:
            prompt: The input prompt for the model.
            temperature: Sampling temperature (ignored in mock).
            max_tokens: Maximum tokens to generate (ignored in mock).

        Returns:
            str: Deterministic mock response.
        """
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()

        if prompt_hash in self._response_cache:
            return self._response_cache[prompt_hash]

        response = self._generate_response(prompt, prompt_hash)
        self._response_cache[prompt_hash] = response
        return response

    async def generate_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        temperature: float = 0.7,
    ) -> dict[str, Any]:
        """
        Generate a deterministic structured mock response.

        Args:
            prompt: The input prompt for the model.
            schema: JSON schema for the expected output structure.
            temperature: Sampling temperature (ignored in mock).

        Returns:
            dict: Deterministic structured mock response.
        """
        prompt_hash = hashlib.md5((prompt + str(schema)).encode()).hexdigest()
        return self._generate_structured_response(schema, prompt_hash)

    def _generate_response(self, prompt: str, prompt_hash: str) -> str:
        """
        Generate a context-aware response based on prompt content.

        Args:
            prompt: The input prompt.
            prompt_hash: Hash of the prompt for determinism.

        Returns:
            str: Generated response.
        """
        prompt_lower = prompt.lower()

        if "protocol" in prompt_lower and "extract" in prompt_lower:
            return self._protocol_extraction_response()
        elif "phi" in prompt_lower and "redact" in prompt_lower:
            return self._phi_redaction_response()
        elif "eligibility" in prompt_lower:
            return self._eligibility_response()
        elif "safety" in prompt_lower:
            return self._safety_response()
        elif "audit" in prompt_lower:
            return self._audit_response()
        else:
            return self._generic_response(prompt)

    def _generate_structured_response(
        self, schema: dict[str, Any], prompt_hash: str
    ) -> dict[str, Any]:
        """
        Generate a structured response matching the schema.

        Args:
            schema: JSON schema for the response.
            prompt_hash: Hash for determinism.

        Returns:
            dict: Structured response.
        """
        result: dict[str, Any] = {}

        for key, value in schema.items():
            if isinstance(value, dict):
                result[key] = self._generate_structured_response(value, prompt_hash)
            elif isinstance(value, str):
                if "confidence" in key.lower():
                    result[key] = 0.85
                elif "score" in key.lower():
                    result[key] = 0.92
                elif "eligible" in key.lower():
                    result[key] = True
                elif "status" in key.lower():
                    result[key] = "approved"
                else:
                    result[key] = f"mock_value_{key}"
            elif isinstance(value, bool):
                result[key] = True
            elif isinstance(value, (int, float)):
                result[key] = value
            else:
                result[key] = None

        return result

    def _protocol_extraction_response(self) -> str:
        """Return mock protocol extraction response."""
        return """Protocol Analysis Results:

Inclusion Criteria:
- Age: 18-75 years
- Diagnosis: Type 2 Diabetes Mellitus
- HbA1c: 7.0-10.0%
- BMI: 25-40 kg/m²
- Stable medication regimen for 3 months

Exclusion Criteria:
- Type 1 Diabetes
- Severe renal impairment (eGFR < 30)
- Active cardiovascular disease
- Pregnancy or breastfeeding
- History of severe hypoglycemia

Study Duration: 24 weeks
Visits Required: 8
Primary Endpoint: Change in HbA1c from baseline"""

    def _phi_redaction_response(self) -> str:
        """Return mock PHI redaction response."""
        return """PHI Redaction Complete:

Fields Redacted:
- Patient Name: [REDACTED]
- Date of Birth: [REDACTED]
- SSN: [REDACTED]
- Address: [REDACTED]
- Phone: [REDACTED]
- Email: [REDACTED]

Medical Information Preserved:
- Age group: 45-54
- Gender: Female
- Diagnosis codes: E11.9
- Lab values: Preserved
- Medication names: Preserved

Compliance: HIPAA/GDPR compliant"""

    def _eligibility_response(self) -> str:
        """Return mock eligibility assessment response."""
        return """Eligibility Assessment:

Patient ID: PATIENT_001
Protocol: DIABETES_TRIAL_2024

Overall Eligibility: ELIGIBLE

Criteria Evaluation:
✓ Age: 52 years (within 18-75)
✓ Diagnosis: Type 2 Diabetes confirmed
✓ HbA1c: 8.2% (within 7.0-10.0)
✓ BMI: 31.5 kg/m² (within 25-40)
✓ Medication stable: Yes (4 months)

Exclusion Check:
✓ No Type 1 Diabetes
✓ No severe renal impairment (eGFR: 58)
✓ No active cardiovascular disease
✓ Not pregnant
✓ No severe hypoglycemia history

Confidence Score: 0.94
Recommendation: Proceed with screening"""

    def _safety_response(self) -> str:
        """Return mock medical safety response."""
        return """Medical Safety Assessment:

Patient Safety Evaluation: SAFE TO PROCEED

Risk Factors:
- Mild hypertension (controlled)
- No known drug allergies
- No contraindications identified

Drug Interactions:
- Current medications: Metformin, Lisinopril
- Study medication: No interactions expected

Lab Safety:
- Liver function: Normal
- Kidney function: Mild impairment (acceptable)
- Blood counts: Within normal limits

Monitoring Recommendations:
- Weekly blood glucose monitoring
- Monthly renal function tests
- Blood pressure monitoring at each visit

Safety Clearance: APPROVED"""

    def _audit_response(self) -> str:
        """Return mock audit response."""
        return """Regulatory Audit Report:

Audit Date: 2024-01-15
Auditor: System Automated Audit

Compliance Status: COMPLIANT

Findings:
✓ Protocol adherence: 100%
✓ PHI protection: Fully compliant
✓ Eligibility criteria: Properly applied
✓ Documentation: Complete
✓ Consent process: Valid
✓ Safety monitoring: Adequate

Regulatory References:
- 21 CFR Part 312: Compliant
- ICH-GCP E6: Compliant
- HIPAA Privacy Rule: Compliant
- GDPR Article 9: Compliant

Recommendations:
- Continue current procedures
- No corrective actions required

Audit Trail ID: AUDIT_2024_001"""

    def _generic_response(self, prompt: str) -> str:
        """Return a generic mock response."""
        return f"Mock response for: {prompt[:100]}..."
