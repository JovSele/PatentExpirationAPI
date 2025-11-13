"""
Rate limiter middleware for API requests.
Tracks usage per API key and enforces tier limits.
"""

from fastapi import Request, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict
from app.config import settings
import hashlib


class RateLimiter:
    """
    Rate limiter for API requests.
    Tracks requests per API key and enforces monthly limits.
    """
    
    def __init__(self):
        # In-memory storage: {api_key_hash: {"count": X, "reset_date": datetime}}
        # For production, use Redis or database
        self.usage: dict = defaultdict(lambda: {"count": 0, "reset_date": None})
        
    def _hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage (privacy)."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def _get_tier_limit(self, tier: str) -> int:
        """Get request limit for tier."""
        tier_limits = {
            "free": settings.rate_limit_free,
            "basic": settings.rate_limit_basic,
            "pro": settings.rate_limit_pro,
            "enterprise": 999999  # Effectively unlimited
        }
        return tier_limits.get(tier.lower(), settings.rate_limit_free)
    
    def _should_reset(self, reset_date: Optional[datetime]) -> bool:
        """Check if counter should be reset (monthly)."""
        if not reset_date:
            return True
        return datetime.now() >= reset_date
    
    def check_rate_limit(
        self, 
        api_key: str, 
        tier: str = "free"
    ) -> tuple[bool, int, int]:
        """
        Check if request is within rate limit.
        
        Args:
            api_key: API key from RapidAPI
            tier: User tier (free, basic, pro, enterprise)
            
        Returns:
            Tuple of (allowed: bool, remaining: int, limit: int)
        """
        key_hash = self._hash_api_key(api_key)
        usage = self.usage[key_hash]
        limit = self._get_tier_limit(tier)
        
        # Reset counter if month has passed
        if self._should_reset(usage["reset_date"]):
            usage["count"] = 0
            usage["reset_date"] = datetime.now() + timedelta(days=30)
        
        # Check limit
        if usage["count"] >= limit:
            return False, 0, limit
        
        # Increment counter
        usage["count"] += 1
        remaining = limit - usage["count"]
        
        return True, remaining, limit
    
    async def __call__(self, request: Request) -> None:
        """
        FastAPI dependency for rate limiting.
        
        Usage:
            @app.get("/api/v1/status", dependencies=[Depends(rate_limiter)])
        """
        # Extract API key from RapidAPI headers
        api_key = request.headers.get("X-RapidAPI-Proxy-Secret") or \
                  request.headers.get("X-RapidAPI-Key") or \
                  "anonymous"
        
        # Extract tier (RapidAPI sends this in headers)
        tier = request.headers.get("X-RapidAPI-Subscription") or "free"
        
        # Check rate limit
        allowed, remaining, limit = self.check_rate_limit(api_key, tier)
        
        # Add rate limit info to response headers
        request.state.rate_limit_remaining = remaining
        request.state.rate_limit_limit = limit
        
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "RateLimitExceeded",
                    "message": f"Monthly limit of {limit} requests exceeded",
                    "limit": limit,
                    "tier": tier,
                    "upgrade_url": "https://rapidapi.com/your-api/pricing"
                }
            )


# Global rate limiter instance
rate_limiter = RateLimiter()
