"""
Global exception handlers for FastAPI.

This module provides handlers for custom and built-in exceptions.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.core.exceptions import (
    AgentExecutionError,
    ApplicationException,
    ComplianceError,
    DataIngestionError,
    ProviderError,
    ValidationError,
)
from backend.core.logging_config import get_logger

logger = get_logger(__name__)


async def application_exception_handler(
    request: Request, exc: ApplicationException
) -> JSONResponse:
    """
    Handle application-specific exceptions.

    Args:
        request: The incoming request.
        exc: The application exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Application error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )


async def provider_exception_handler(request: Request, exc: ProviderError) -> JSONResponse:
    """
    Handle provider-related exceptions.

    Args:
        request: The incoming request.
        exc: The provider exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Provider error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "ProviderError",
            "message": "AI provider service unavailable",
            "details": exc.details,
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle validation exceptions.

    Args:
        request: The incoming request.
        exc: The validation exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.warning(
        f"Validation error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def agent_execution_exception_handler(
    request: Request, exc: AgentExecutionError
) -> JSONResponse:
    """
    Handle agent execution exceptions.

    Args:
        request: The incoming request.
        exc: The agent execution exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Agent execution error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "AgentExecutionError",
            "message": "Agent execution failed",
            "details": exc.details,
        },
    )


async def data_ingestion_exception_handler(
    request: Request, exc: DataIngestionError
) -> JSONResponse:
    """
    Handle data ingestion exceptions.

    Args:
        request: The incoming request.
        exc: The data ingestion exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Data ingestion error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "DataIngestionError",
            "message": exc.message,
            "details": exc.details,
        },
    )


async def compliance_exception_handler(request: Request, exc: ComplianceError) -> JSONResponse:
    """
    Handle compliance exceptions.

    Args:
        request: The incoming request.
        exc: The compliance exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Compliance error: {exc.message}",
        extra={"details": exc.details, "path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "ComplianceError",
            "message": "Compliance check failed",
            "details": exc.details,
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions.

    Args:
        request: The incoming request.
        exc: The HTTP exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.warning(
        f"HTTP error: {exc.status_code} - {exc.detail}",
        extra={"path": request.url.path},
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPError",
            "message": exc.detail,
            "status_code": exc.status_code,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all unhandled exceptions.

    Args:
        request: The incoming request.
        exc: The unhandled exception.

    Returns:
        JSONResponse: Formatted error response.
    """
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
        },
    )
