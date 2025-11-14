"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime
import re


class PatentStatusRequest(BaseModel):
    """Request schema for patent status lookup."""
    patent: str = Field(..., description="Patent number (e.g., EP1234567, US7654321)")
    
    @validator('patent')
    def validate_patent_format(cls, v):
        """Validate patent number format."""
        # Remove spaces and convert to uppercase
        v = v.strip().upper().replace(" ", "")
        
        # Basic validation for EP and US patents
        if not re.match(r'^(EP|US)\d{7,}', v):
            raise ValueError(
                "Invalid patent format. Expected format: EP1234567 or US7654321"
            )
        
        return v


class PatentStatusResponse(BaseModel):
    patent_number: str
    status: str
    expiry_date: Optional[str]
    jurisdictions: Optional[Dict[str, str]]  # ← ZMEŇ z List[str] na Dict[str, str]
    lapse_reason: Optional[str]
    source: str
    last_fetched: Optional[str]
    cache_hit: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "patent": "EP1234567",
                "status": "expired",
                "expiry_date": "2021-11-04",
                "jurisdictions": ["EP", "DE", "FR"],
                "lapse_reason": "fee not paid",
                "source": "EPO",
                "last_update": "2025-11-11T10:30:00Z",
                "disclaimer": "For informational purposes only. Not legal advice."
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid patent format",
                "detail": "Expected format: EP1234567 or US7654321"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current timestamp")
    database: str = Field(..., description="Database connection status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2025-11-11T10:30:00Z",
                "database": "connected"
            }
        }
