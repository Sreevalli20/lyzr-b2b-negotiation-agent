"""
Middleware module for FastAPI.

This module exports all middleware components.
"""

from backend.middleware.cors import get_cors_middleware
from backend.middleware.logging import LoggingMiddleware

__all__ = ["LoggingMiddleware", "get_cors_middleware"]
