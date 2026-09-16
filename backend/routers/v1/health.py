"""
Health check endpoints.

This module provides health check endpoints for the API.
"""

from fastapi import APIRouter

from backend.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Current health status of the service.
    """
    return HealthResponse(status="healthy")


@router.get("/health/ready", response_model=HealthResponse)
async def readiness_check() -> HealthResponse:
    """
    Readiness check endpoint.

    Returns:
        HealthResponse: Readiness status of the service.
    """
    return HealthResponse(status="ready")


@router.get("/health/live", response_model=HealthResponse)
async def liveness_check() -> HealthResponse:
    """
    Liveness check endpoint.

    Returns:
        HealthResponse: Liveness status of the service.
    """
    return HealthResponse(status="alive")
