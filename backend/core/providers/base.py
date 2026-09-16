"""
Base provider interfaces for AI services.

This module defines abstract interfaces for LLM and Lyzr providers,
enabling dependency injection and easy switching between mock and real implementations.
"""

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    This interface defines the contract for language model providers,
    allowing seamless switching between different implementations.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt: The input prompt for the model.
            temperature: Sampling temperature (0.0 to 1.0).
            max_tokens: Maximum tokens to generate.

        Returns:
            str: Generated response text.
        """
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: dict[str, Any],
        temperature: float = 0.7,
    ) -> dict[str, Any]:
        """
        Generate a structured JSON response from the language model.

        Args:
            prompt: The input prompt for the model.
            schema: JSON schema for the expected output structure.
            temperature: Sampling temperature (0.0 to 1.0).

        Returns:
            dict: Structured response matching the schema.
        """
        pass


class LyzrProvider(ABC):
    """
    Abstract base class for Lyzr agent providers.

    This interface defines the contract for Lyzr agent interactions,
    enabling mock and real implementations.
    """

    @abstractmethod
    async def create_agent(
        self,
        agent_type: str,
        config: dict[str, Any],
    ) -> str:
        """
        Create a new agent instance.

        Args:
            agent_type: Type of agent to create.
            config: Agent configuration parameters.

        Returns:
            str: Agent ID.
        """
        pass

    @abstractmethod
    async def execute_agent(
        self,
        agent_id: str,
        input_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute an agent with input data.

        Args:
            agent_id: ID of the agent to execute.
            input_data: Input data for the agent.

        Returns:
            dict: Agent execution result.
        """
        pass

    @abstractmethod
    async def get_agent_status(self, agent_id: str) -> dict[str, Any]:
        """
        Get the status of an agent.

        Args:
            agent_id: ID of the agent.

        Returns:
            dict: Agent status information.
        """
        pass
