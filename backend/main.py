"""
Main FastAPI application entry point.

This module initializes the FastAPI application and includes all routers.
"""

from fastapi import FastAPI
from backend.api.router import api_router
from backend.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="Governed Clinical Trial Patient Screening & Regulatory Audit Agent",
        description="Enterprise-grade AI agent for clinical trial patient screening and regulatory compliance auditing.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

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
            "status": "Repository initialized",
            "competition": "HiDevs AI Quest 2026",
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
