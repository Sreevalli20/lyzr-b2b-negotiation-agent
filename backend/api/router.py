"""
API router module with versioning.

This module aggregates all API routers for the application with version support.
"""

from fastapi import APIRouter

api_router = APIRouter()

# Version 1 routers (imported after router creation to avoid circular imports)
from backend.routers.v1 import agents, audit, eligibility, health, phi  # noqa: E402

api_router.include_router(health.router, prefix="/v1", tags=["health"])
api_router.include_router(agents.router, prefix="/v1", tags=["agents"])
api_router.include_router(eligibility.router, prefix="/v1", tags=["eligibility"])
api_router.include_router(phi.router, prefix="/v1", tags=["phi"])
api_router.include_router(audit.router, prefix="/v1", tags=["audit"])


@api_router.get("/")
async def api_root() -> dict[str, str]:
    """
    API root endpoint.

    Returns:
        dict: API information.
    """
    return {
        "message": "Clinical Trial Patient Screening & Regulatory Audit API",
        "version": "1.0.0",
        "status": "operational",
    }
