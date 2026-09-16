"""
API router module.

This module aggregates all API routers for the application.
"""

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
async def api_root() -> dict[str, str]:
    """
    API root endpoint.

    Returns:
        dict: API information.
    """
    return {"message": "API v1.0"}
