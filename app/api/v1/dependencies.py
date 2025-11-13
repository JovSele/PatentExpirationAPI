"""
API dependencies for FastAPI endpoints.
Provides shared functionality like database sessions and service instances.
"""

from typing import Generator
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.epo_service import EPOService
from app.services.uspto_service import USPTOService
from app.services.cache_service import CacheService
from app.config import settings


def get_epo_service() -> EPOService:
    """Dependency to get EPO service instance."""
    return EPOService()


def get_uspto_service() -> USPTOService:
    """Dependency to get USPTO service instance."""
    return USPTOService()


def get_cache_service() -> CacheService:
    """Dependency to get cache service instance."""
    return CacheService()


def verify_rapidapi_secret(
    x_rapidapi_proxy_secret: str = Header(None)
) -> str:
    """
    Verify RapidAPI proxy secret.
    Optional security layer for RapidAPI integration.
    """
    if not settings.rapidapi_proxy_secret:
        # Secret not configured, skip verification
        return "not_configured"
    
    if x_rapidapi_proxy_secret != settings.rapidapi_proxy_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid RapidAPI proxy secret"
        )
    
    return x_rapidapi_proxy_secret
