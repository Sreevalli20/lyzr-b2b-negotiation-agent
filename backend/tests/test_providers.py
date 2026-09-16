"""
Tests for AI providers.

This module contains tests for mock LLM and Lyzr providers.
"""

import pytest

from backend.core.providers.mock_llm import MockLLMProvider
from backend.core.providers.mock_lyzr import MockLyzrProvider


@pytest.mark.asyncio
class TestMockLLMProvider:
    """Test suite for MockLLMProvider."""

    @pytest.fixture
    def provider(self) -> MockLLMProvider:
        """Fixture for MockLLMProvider instance."""
        return MockLLMProvider()

    async def test_generate_basic(self, provider: MockLLMProvider) -> None:
        """Test basic text generation."""
        prompt = "Test prompt"
        response = await provider.generate(prompt)
        assert isinstance(response, str)
        assert len(response) > 0

    async def test_generate_deterministic(self, provider: MockLLMProvider) -> None:
        """Test that responses are deterministic."""
        prompt = "Test prompt"
        response1 = await provider.generate(prompt)
        response2 = await provider.generate(prompt)
        assert response1 == response2

    async def test_generate_protocol_extraction(self, provider: MockLLMProvider) -> None:
        """Test protocol extraction response."""
        prompt = "Extract protocol information"
        response = await provider.generate(prompt)
        assert "Protocol Analysis Results" in response

    async def test_generate_phi_redaction(self, provider: MockLLMProvider) -> None:
        """Test PHI redaction response."""
        prompt = "Redact PHI from text"
        response = await provider.generate(prompt)
        assert "PHI Redaction Complete" in response

    async def test_generate_structured(self, provider: MockLLMProvider) -> None:
        """Test structured response generation."""
        prompt = "Test prompt"
        schema = {"confidence": 0.85, "eligible": True}
        response = await provider.generate_structured(prompt, schema)
        assert isinstance(response, dict)
        assert "confidence" in response
        assert "eligible" in response


@pytest.mark.asyncio
class TestMockLyzrProvider:
    """Test suite for MockLyzrProvider."""

    @pytest.fixture
    def provider(self) -> MockLyzrProvider:
        """Fixture for MockLyzrProvider instance."""
        return MockLyzrProvider()

    async def test_create_agent(self, provider: MockLyzrProvider) -> None:
        """Test agent creation."""
        agent_id = await provider.create_agent("eligibility", {})
        assert agent_id.startswith("mock_agent_eligibility_")

    async def test_execute_agent(self, provider: MockLyzrProvider) -> None:
        """Test agent execution."""
        agent_id = await provider.create_agent("eligibility", {})
        result = await provider.execute_agent(agent_id, {"patient_id": "123"})
        assert isinstance(result, dict)
        assert "status" in result

    async def test_get_agent_status(self, provider: MockLyzrProvider) -> None:
        """Test getting agent status."""
        agent_id = await provider.create_agent("eligibility", {})
        status = await provider.get_agent_status(agent_id)
        assert isinstance(status, dict)
        assert "agent_id" in status
        assert status["agent_id"] == agent_id

    async def test_execute_ingestion_agent(self, provider: MockLyzrProvider) -> None:
        """Test ingestion agent execution."""
        agent_id = await provider.create_agent("ingestion", {})
        result = await provider.execute_agent(agent_id, {"data_type": "ehr"})
        assert result["status"] == "success"
        assert "validation" in result

    async def test_execute_eligibility_agent(self, provider: MockLyzrProvider) -> None:
        """Test eligibility agent execution."""
        agent_id = await provider.create_agent("eligibility", {})
        result = await provider.execute_agent(agent_id, {"patient_id": "123"})
        assert result["status"] == "success"
        assert "eligible" in result

    async def test_execute_audit_agent(self, provider: MockLyzrProvider) -> None:
        """Test audit agent execution."""
        agent_id = await provider.create_agent("audit", {})
        result = await provider.execute_agent(agent_id, {"patient_id": "123"})
        assert result["status"] == "success"
        assert "compliance_status" in result

    async def test_nonexistent_agent(self, provider: MockLyzrProvider) -> None:
        """Test error handling for nonexistent agent."""
        with pytest.raises(ValueError, match="Agent .* not found"):
            await provider.execute_agent("nonexistent", {})
