"""
Logging middleware for FastAPI.

This middleware logs all HTTP requests and responses with timing information.
"""

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.core.logging_config import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log HTTP requests and responses.

    Logs request method, path, status code, and processing time.
    Adds a unique request ID for tracing.
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        Initialize the logging middleware.

        Args:
            app: The ASGI application.
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request and log details.

        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            Response: The response from the next handler.
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Record start time
        start_time = time.time()

        # Log request
        logger.info(
            f"Request started | ID: {request_id} | "
            f"Method: {request.method} | Path: {request.url.path}"
        )

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"Request failed | ID: {request_id} | " f"Error: {str(e)}",
                exc_info=True,
            )
            raise

        # Calculate processing time
        process_time = time.time() - start_time

        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        # Log response
        logger.info(
            f"Request completed | ID: {request_id} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.3f}s"
        )

        return response
