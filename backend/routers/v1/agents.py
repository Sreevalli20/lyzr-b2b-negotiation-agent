"""
Agent execution endpoints.

This module provides endpoints for executing AI agents.
"""

from fastapi import APIRouter, Depends

from backend.core.providers.base import LyzrProvider
from backend.dependencies.providers import get_lyzr_provider
from backend.schemas.agent import (
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentStatus,
)

router = APIRouter()


@router.post("/agents/execute", response_model=AgentExecutionResult)
async def execute_agent(
    request: AgentExecutionRequest,
    lyzr_provider: LyzrProvider = Depends(get_lyzr_provider),
) -> AgentExecutionResult:
    """
    Execute an AI agent with the provided input data.

    Args:
        request: Agent execution request with input data.
        lyzr_provider: Injected Lyzr provider instance.

    Returns:
        AgentExecutionResult: Result of agent execution.
    """
    import time

    start_time = time.time()

    agent_id = await lyzr_provider.create_agent(
        agent_type=request.agent_type,
        config=request.config.dict() if request.config else {},
    )

    result = await lyzr_provider.execute_agent(
        agent_id=agent_id,
        input_data=request.input_data,
    )

    execution_time = int((time.time() - start_time) * 1000)

    return AgentExecutionResult(
        agent_id=agent_id,
        agent_type=request.agent_type,
        status=result.get("status", "completed"),
        output_data=result,
        execution_time_ms=execution_time,
    )


@router.get("/agents/{agent_id}/status", response_model=AgentStatus)
async def get_agent_status(
    agent_id: str,
    lyzr_provider: LyzrProvider = Depends(get_lyzr_provider),
) -> AgentStatus:
    """
    Get the status of an agent.

    Args:
        agent_id: ID of the agent.
        lyzr_provider: Injected Lyzr provider instance.

    Returns:
        AgentStatus: Current status of the agent.
    """
    status = await lyzr_provider.get_agent_status(agent_id)

    return AgentStatus(
        agent_id=agent_id,
        agent_type=status.get("type", "unknown"),
        status=status.get("status", "unknown"),
        created_at=status.get("created_at", ""),
        last_execution=status.get("last_execution"),
        total_executions=0,
    )
