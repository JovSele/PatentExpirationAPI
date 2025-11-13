"""
Main FastAPI application.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.config import settings
from app.database import init_db
from app.api.v1 import endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Initialize database on startup.
    """
    # Startup
    print("🚀 Starting Patent Expiration API...")
    init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Patent Expiration API...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="""
    **Patent Expiration API** - B2B Micro-Service for checking patent status.
    
    ## Features
    - ✅ Single patent lookup (EP, US)
    - ✅ Status: active/expired
    - ✅ Expiry date & jurisdictions
    - ✅ Lapse reason tracking
    - ✅ 30-day cache (fast responses)
    - ✅ Rate limiting by tier
    
    ## Supported Patents
    - **European Patents:** EP1234567
    - **US Patents:** US7654321
    
    ## Rate Limits
    - **Free:** 20 requests/month
    - **Basic:** 1,000 requests/month (€19)
    - **Pro:** 10,000 requests/month (€99)
    
    ## Legal Disclaimer
    ⚠️ This API provides information **for informational purposes only**.
    Not legal advice. Always verify critical information with official patent offices.
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Middleware for adding rate limit headers to response
@app.middleware("http")
async def add_rate_limit_headers(request: Request, call_next):
    """Add rate limit info to response headers."""
    response = await call_next(request)
    
    # Add rate limit headers if available
    if hasattr(request.state, "rate_limit_remaining"):
        response.headers["X-RateLimit-Remaining"] = str(request.state.rate_limit_remaining)
        response.headers["X-RateLimit-Limit"] = str(request.state.rate_limit_limit)
    
    return response


# Middleware for request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
    return response


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": "Endpoint not found",
            "detail": f"The requested URL {request.url.path} was not found"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else "Please try again later"
        }
    )


# Include routers
app.include_router(
    endpoints.router,
    prefix="/api/v1",
    tags=["Patents"]
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API info.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs",
        "health_check": "/api/v1/health",
        "endpoints": {
            "patent_status": "/api/v1/status?patent=EP1234567"
        },
        "legal_disclaimer": "For informational purposes only. Not legal advice."
    }


# Legal disclaimer endpoint
@app.get("/disclaimer", tags=["Legal"])
async def legal_disclaimer():
    """
    Legal disclaimer and terms of use.
    """
    return {
        "disclaimer": """
        LEGAL DISCLAIMER
        
        This API provides patent status information FOR INFORMATIONAL PURPOSES ONLY.
        
        NO WARRANTY:
        - Information is provided "as is" without warranty of any kind
        - We do not guarantee accuracy, completeness, or timeliness
        - Data depends on external sources (EPO, USPTO) which may be incorrect or outdated
        
        NOT LEGAL ADVICE:
        - This service does NOT constitute legal advice
        - Do NOT rely solely on this API for critical patent decisions
        - Always consult a qualified patent attorney for legal matters
        
        LIMITATION OF LIABILITY:
        - We are not liable for any damages arising from use of this API
        - Users assume all risks associated with using this service
        
        VERIFICATION REQUIRED:
        - Always verify critical patent information with official patent offices:
          * EPO: https://www.epo.org
          * USPTO: https://www.uspto.gov
        
        By using this API, you acknowledge and agree to these terms.
        """,
        "last_updated": "2025-11-13",
        "contact": "support@yourservice.com"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
