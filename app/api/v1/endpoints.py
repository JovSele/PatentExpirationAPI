"""
API endpoints for patent status lookup.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import time

from app.schemas import (
    PatentStatusResponse,
    ErrorResponse,
    HealthCheckResponse
)
from app.database import get_db
from app.services.patent_service import PatentService
from app.api.v1.dependencies import get_patent_service
from app.utils.rate_limiter import rate_limiter
from app.config import settings
from app.models import RequestLog

router = APIRouter()


@router.get(
    "/status",
    response_model=PatentStatusResponse,
    responses={
        200: {"description": "Patent status retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid patent format"},
        404: {"model": ErrorResponse, "description": "Patent not found"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Patent Status",
    description="""
    Retrieve patent status information including:
    - Current status (active/expired)
    - Expiry date
    - Active jurisdictions
    - Lapse reason (if expired)
    
    Supported patent formats:
    - European: EP1234567
    - US: US7654321
    """,
    dependencies=[Depends(rate_limiter)]
)
async def get_patent_status(
    request: Request,
    patent: str = Query(...),
    db: Session = Depends(get_db),
    patent_service: PatentService = Depends(get_patent_service)
):
    """
    Get patent status with caching.
    
    Flow:
    1. Check cache
    2. If cache miss or stale → fetch from API
    3. Normalize data
    4. Store in cache
    5. Return response
    """
    start_time = time.time()
    cache_hit = False
    
    try:
        # Normalize patent number
        patent = patent.strip().upper().replace(" ", "")
        
        # Validate format
        if not patent.startswith(("EP", "US")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "message": "Invalid patent format",
                    "detail": "Expected format: EP1234567 or US7654321"
                }
            )
        
        # Get patent status using unified service (handles cache, EPO, Lens, USPTO)
        patent_data = await patent_service.get_patent_status(db, patent)
        
        if not patent_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "NotFound",
                    "message": "Patent not found",
                    "detail": f"Patent {patent} not found in any data source"
                }
            )
        
        # Extract cache hit info
        cache_hit = patent_data.pop("cache_hit", False)
        
        # Log request
        response_time_ms = int((time.time() - start_time) * 1000)
        _log_request(
            db=db,
            request=request,
            patent_number=patent,
            status_code=200,
            response_time_ms=response_time_ms,
            cache_hit=cache_hit
        )
        
        # Build response
        response = PatentStatusResponse(
            patent_number=patent_data["patent_number"],
            status=patent_data["status"],
            expiry_date=patent_data.get("expiry_date"),
            jurisdictions=patent_data.get("jurisdictions"),
            lapse_reason=patent_data.get("lapse_reason"),
            source=patent_data["source"],
            last_fetched=patent_data.get("last_fetched", datetime.now().isoformat()),
            cache_hit=cache_hit
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error
        response_time_ms = int((time.time() - start_time) * 1000)
        _log_request(
            db=db,
            request=request,
            patent_number=patent,
            status_code=500,
            response_time_ms=response_time_ms,
            cache_hit=False
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Failed to retrieve patent status",
                "detail": str(e) if settings.debug else "Please try again later"
            }
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check API health and database connectivity"
)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    Returns API status and version.
    """
    # Test database connection
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return HealthCheckResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.app_version,
        timestamp=datetime.now().isoformat(),
        database=db_status
    )


def _log_request(
    db: Session,
    request: Request,
    patent_number: str,
    status_code: int,
    response_time_ms: int,
    cache_hit: bool
):
    """Log API request for analytics."""
    try:
        # Extract headers
        api_key = request.headers.get("X-RapidAPI-Proxy-Secret") or \
                  request.headers.get("X-RapidAPI-Key")
        tier = request.headers.get("X-RapidAPI-Subscription", "free")
        ip = request.client.host if request.client else None
        user_agent = request.headers.get("User-Agent")
        
        # Hash API key for privacy
        api_key_hash = None
        if api_key:
            import hashlib
            api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Create log entry
        log_entry = RequestLog(
            patent_number=patent_number,
            endpoint=str(request.url.path),
            method=request.method,
            api_key_hash=api_key_hash,
            user_tier=tier,
            status_code=status_code,
            response_time_ms=response_time_ms,
            cache_hit=cache_hit,
            ip_address=ip,
            user_agent=user_agent
        )
        
        db.add(log_entry)
        db.commit()
    except Exception:
        # Don't fail request if logging fails
        db.rollback()
