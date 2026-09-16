"""
Dependency injection for AI providers.

This module provides factory functions for creating provider instances,
enabling easy switching between mock and real implementations based on configuration.
"""

from backend.core.providers.base import LLMProvider, LyzrProvider
from backend.core.providers.mock_llm import MockLLMProvider
from backend.core.providers.mock_lyzr import MockLyzrProvider


def get_llm_provider() -> LLMProvider:
    """
    Get the configured LLM provider instance.

    Returns:
        LLMProvider: Configured LLM provider (mock or real).

    Note:
        Currently returns MockLLMProvider. When GOOGLE_AI_API_KEY is configured,
        this will return a real Google AI provider implementation.
    """
    return MockLLMProvider()


def get_lyzr_provider() -> LyzrProvider:
    """
    Get the configured Lyzr provider instance.

    Returns:
        LyzrProvider: Configured Lyzr provider (mock or real).

    Note:
        Currently returns MockLyzrProvider. When LYZR_API_KEY is configured,
        this will return a real Lyzr provider implementation.
    """
    return MockLyzrProvider()
