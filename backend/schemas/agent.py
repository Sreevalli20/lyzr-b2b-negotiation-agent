"""
Agent-related Pydantic schemas.

This module defines schemas for agent operations and responses.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Agent configuration parameters."""

    agent_type: str = Field(..., description="Type of agent")
    model_name: str = Field(..., description="AI model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Sampling temperature")
    max_tokens: int = Field(default=1000, ge=1, description="Maximum tokens")
    custom_parameters: dict[str, Any] = Field(default_factory=dict)


class AgentExecutionRequest(BaseModel):
    """Request for agent execution."""

    agent_type: str = Field(..., description="Type of agent to execute")
    input_data: dict[str, Any] = Field(..., description="Input data for agent")
    config: AgentConfig | None = Field(None, description="Agent configuration")


class AgentExecutionResult(BaseModel):
    """Result of agent execution."""

    agent_id: str = Field(..., description="Agent identifier")
    agent_type: str = Field(..., description="Type of agent")
    status: str = Field(..., description="Execution status")
    output_data: dict[str, Any] = Field(..., description="Agent output")
    execution_time_ms: int = Field(..., ge=0, description="Execution time in milliseconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentStatus(BaseModel):
    """Agent status information."""

    agent_id: str = Field(..., description="Agent identifier")
    agent_type: str = Field(..., description="Type of agent")
    status: str = Field(..., description="Agent status")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_execution: datetime | None = Field(None, description="Last execution timestamp")
    total_executions: int = Field(default=0, ge=0, description="Total executions count")
