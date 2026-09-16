"""
Custom exception classes for the application.

This module defines application-specific exceptions for better error handling.
"""


class ApplicationException(Exception):  # noqa: N818
    """Base exception for application-specific errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        """
        Initialize the application exception.

        Args:
            message: Error message.
            details: Additional error details.
        """
        self.message = message
        self.details = details or {}
        super().__init__(message)


class ProviderError(ApplicationException):
    """Exception raised when AI provider operations fail."""

    pass


class ValidationError(ApplicationException):
    """Exception raised when data validation fails."""

    pass


class AgentExecutionError(ApplicationException):
    """Exception raised when agent execution fails."""

    pass


class DataIngestionError(ApplicationException):
    """Exception raised when data ingestion fails."""

    pass


class ComplianceError(ApplicationException):
    """Exception raised when compliance checks fail."""

    pass
