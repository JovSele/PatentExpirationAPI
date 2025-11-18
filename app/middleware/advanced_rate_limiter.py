"""
Advanced rate limiter with API key support and tiered limits.
"""

from fastapi import Request, HTTPException, status
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import hashlib

from app.config import settings
from app.exceptions import RateLimitExceededException


class APIKeyRateLimiter:
    """
    Rate limiter with API key support.
    
    Tiers:
    - Free: 20 requests/month
    - Basic: 1000 requests/month  
    - Pro: 10000 requests/month
    """
    
    def __init__(self):
        # In-memory storage: {api_key_hash: {"count": int, "reset_at": datetime}}
        self.requests: Dict[str, Dict] = defaultdict(lambda: {
            "count": 0,
            "reset_at": datetime.now() + timedelta(days=30)
        })
        
        # Tier limits (requests per month)
        self.tier_limits = {
            "free": settings.rate_limit_free,
            "basic": settings.rate_limit_basic,
            "pro": settings.rate_limit_pro
        }
    
    def _get_api_key_hash(self, request: Request) -> Optional[str]:
        """Extract and hash API key from request headers."""
        # Try different header formats
        api_key = (
            request.headers.get("X-API-Key") or
            request.headers.get("X-RapidAPI-Key") or
            request.headers.get("X-RapidAPI-Proxy-Secret")
        )
        
        if not api_key:
            return None
        
        # Hash for privacy
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def _get_user_tier(self, request: Request) -> str:
        """Get user tier from headers."""
        return request.headers.get("X-RapidAPI-Subscription", "free").lower()
    
    def _get_limit(self, tier: str) -> int:
        """Get rate limit for tier."""
        return self.tier_limits.get(tier, self.tier_limits["free"])
    
    async def check_rate_limit(self, request: Request):
        """
        Check if request is within rate limit.
        Raises RateLimitExceededException if limit exceeded.
        """
        # Get API key hash
        api_key_hash = self._get_api_key_hash(request)
        
        # No API key = use IP-based rate limiting (free tier)
        if not api_key_hash:
            api_key_hash = request.client.host if request.client else "unknown"
        
        # Get user tier and limit
        tier = self._get_user_tier(request)
        limit = self._get_limit(tier)
        
        # Get or create request counter
        now = datetime.now()
        user_data = self.requests[api_key_hash]
        
        # Reset if period expired
        if now >= user_data["reset_at"]:
            user_data["count"] = 0
            user_data["reset_at"] = now + timedelta(days=30)
        
        # Check limit
        if user_data["count"] >= limit:
            reset_time = user_data["reset_at"].isoformat()
            raise RateLimitExceededException(tier, limit, reset_time)
        
        # Increment counter
        user_data["count"] += 1
        
        # Add rate limit headers to response
        request.state.rate_limit_info = {
            "limit": limit,
            "remaining": limit - user_data["count"],
            "reset": user_data["reset_at"].isoformat()
        }


# Global instance
api_key_rate_limiter = APIKeyRateLimiter()