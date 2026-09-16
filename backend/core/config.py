"""
Application configuration module.

This module manages all application settings and environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        APP_NAME: Application name.
        DEBUG: Debug mode flag.
        HOST: Server host address.
        PORT: Server port.
        LYZR_API_KEY: Lyzr API key for AI services.
        GOOGLE_AI_API_KEY: Google AI Studio API key for Gemini.
    """

    APP_NAME: str = "Governed Clinical Trial Patient Screening & Regulatory Audit Agent"
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    LYZR_API_KEY: str = Field(default="", description="Lyzr API key")
    GOOGLE_AI_API_KEY: str = Field(default="", description="Google AI Studio API key")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
