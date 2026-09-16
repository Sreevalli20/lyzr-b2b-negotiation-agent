"""
CORS middleware configuration.

This module provides CORS configuration for the FastAPI application.
"""

from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings


def get_cors_middleware() -> CORSMiddleware:
    """
    Get configured CORS middleware.

    Returns:
        CORSMiddleware: Configured CORS middleware instance.
    """
    return CORSMiddleware(
        allow_origins=["*"] if settings.DEBUG else ["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
