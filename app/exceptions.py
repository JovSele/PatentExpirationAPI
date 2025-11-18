"""
Custom exceptions for Patent Expiration API
"""

from fastapi import HTTPException, status


class PatentAPIException(HTTPException):
    """Base exception for all patent API errors."""
    
    def __init__(
        self,
        status_code: int,
        error: str,
        message: str,
        detail: str = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "message": message,
                "detail": detail
            }
        )


class PatentNotFoundException(PatentAPIException):
    """Patent not found in any data source."""
    
    def __init__(self, patent_number: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error="NotFound",
            message="Patent not found",
            detail=f"Patent {patent_number} not found in any data source (EPO, USPTO)"
        )


class InvalidPatentFormatException(PatentAPIException):
    """Invalid patent number format."""
    
    def __init__(self, patent_number: str, expected_format: str = "EP1234567 or US7654321"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error="ValidationError",
            message="Invalid patent format",
            detail=f"Patent '{patent_number}' has invalid format. Expected: {expected_format}"
        )


class RateLimitExceededException(PatentAPIException):
    """Rate limit exceeded for API key."""
    
    def __init__(self, tier: str, limit: int, reset_time: str = None):
        detail = f"Rate limit ({limit} requests) exceeded for tier '{tier}'"
        if reset_time:
            detail += f". Resets at {reset_time}"
        
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error="RateLimitExceeded",
            message="Too many requests",
            detail=detail
        )


class ExternalAPIException(PatentAPIException):
    """External API (EPO/USPTO/Lens) error."""
    
    def __init__(self, source: str, error_message: str):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error="ExternalAPIError",
            message=f"{source} API error",
            detail=error_message
        )


class DatabaseException(PatentAPIException):
    """Database operation error."""
    
    def __init__(self, operation: str, error_message: str = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="DatabaseError",
            message=f"Database {operation} failed",
            detail=error_message if error_message else "Please try again later"
        )


class InvalidAPIKeyException(PatentAPIException):
    """Invalid or missing API key."""
    
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="Unauthorized",
            message="Invalid or missing API key",
            detail="Please provide a valid API key in X-API-Key header"
        )