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
# STARÉ (PROBLÉMOVÉ) IMPORTY: from app.api.v1 import endpoints, analytics 
from app.api.v1.endpoints import router as endpoints_router # NOVÉ SPRÁVNE IMPORTY (Musia byť definované takto v app/api/v1/__init__.py)
from app.api.v1.analytics import router as analytics_router # NOVÉ SPRÁVNE IMPORTY (Musia byť definované takto v app/api/v1/__init__.py)

from app.middleware.advanced_rate_limiter import api_key_rate_limiter
from app.exceptions import RateLimitExceededException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
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
    - ✅ 30-day cache (fast responses)
    - ✅ Rate limiting by tier
    
    ## Supported Patents
    - **European Patents:** EP1234567
    - **US Patents:** US7654321
    
    ## Rate Limits
    - **Free:** 20 requests/month
    - **Basic:** 1,000 requests/month
    - **Pro:** 10,000 requests/month
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


# Rate limit middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip for health check and analytics
    if request.url.path in ["/api/v1/health", "/", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)
    
    # Check rate limit
    try:
        await api_key_rate_limiter.check_rate_limit(request)
    except RateLimitExceededException as e:
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail,
            headers={
                "X-RateLimit-Limit": str(request.state.rate_limit_info["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": request.state.rate_limit_info["reset"]
            }
        )
    
    # Process request
    response = await call_next(request)
    
    # Add rate limit headers
    if hasattr(request.state, "rate_limit_info"):
        info = request.state.rate_limit_info
        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = info["reset"]
    
    return response


# Request timing middleware
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
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": "Endpoint not found",
            "detail": f"The requested URL {request.url.path} was not found"
        }
    )


# Include routers (Použite nové názvy premenných)
app.include_router(endpoints_router, prefix="/api/v1", tags=["Patents"])
app.include_router(analytics_router, prefix="/api/v1", tags=["Analytics"])

# Include routers
# app.include_router(endpoints.router, prefix="/api/v1", tags=["Patents"])
# app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs",
        "endpoints": {
            "patent_status": "/api/v1/status?patent=EP1234567",
            "analytics": "/api/v1/stats/overview"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=True)