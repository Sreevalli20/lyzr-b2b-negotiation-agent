"""
Main FastAPI application entry point.

This module initializes the FastAPI application with all middleware,
exception handlers, and routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.api.router import api_router
from backend.core.config import settings
from backend.core.exception_handlers import (
    agent_execution_exception_handler,
    application_exception_handler,
    compliance_exception_handler,
    data_ingestion_exception_handler,
    general_exception_handler,
    http_exception_handler,
    provider_exception_handler,
    validation_exception_handler,
)
from backend.core.exceptions import (
    AgentExecutionError,
    ApplicationException,
    ComplianceError,
    DataIngestionError,
    ProviderError,
    ValidationError,
)
from backend.core.logging_config import setup_logging
from backend.middleware import LoggingMiddleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    # Setup logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title="Governed Clinical Trial Patient Screening & Regulatory Audit Agent",
        description="Enterprise-grade AI agent for clinical trial patient screening and regulatory compliance auditing.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else ["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    # Register exception handlers
    app.add_exception_handler(ApplicationException, application_exception_handler)
    app.add_exception_handler(ProviderError, provider_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(AgentExecutionError, agent_execution_exception_handler)
    app.add_exception_handler(DataIngestionError, data_ingestion_exception_handler)
    app.add_exception_handler(ComplianceError, compliance_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Include API router
    app.include_router(api_router, prefix="/api")

    @app.get("/")
    async def root() -> dict[str, str]:
        """
        Root endpoint returning project information.

        Returns:
            dict: Project metadata and status.
        """
        return {
            "project": "Governed Clinical Trial Patient Screening & Regulatory Audit Agent",
            "status": "Production-ready offline foundation",
            "competition": "HiDevs AI Quest 2026",
            "version": "1.0.0",
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        """
        Health check endpoint.

        Returns:
            dict: Health status.
        """
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
