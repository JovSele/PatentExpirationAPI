"""
Analytics endpoints for monitoring API usage.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models import RequestLog, PatentCache


router = APIRouter()


@router.get("/stats/overview")
async def get_overview_stats(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to analyze")
):
    """Get overall API usage statistics."""
    
    since = datetime.now() - timedelta(days=days)
    
    # Total requests
    total_requests = db.query(func.count(RequestLog.id)).filter(
        RequestLog.created_at >= since
    ).scalar()
    
    # Cache hit rate
    cache_hits = db.query(func.count(RequestLog.id)).filter(
        RequestLog.created_at >= since,
        RequestLog.cache_hit == True
    ).scalar()
    
    cache_hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
    
    # Average response time
    avg_response_time = db.query(func.avg(RequestLog.response_time_ms)).filter(
        RequestLog.created_at >= since
    ).scalar() or 0
    
    # Requests by status code
    status_codes = db.query(
        RequestLog.status_code,
        func.count(RequestLog.id).label('count')
    ).filter(
        RequestLog.created_at >= since
    ).group_by(RequestLog.status_code).all()
    
    # Top patents
    top_patents = db.query(
        PatentCache.patent_number,
        PatentCache.fetch_count
    ).order_by(desc(PatentCache.fetch_count)).limit(10).all()
    
    return {
        "period_days": days,
        "total_requests": total_requests,
        "cache_hits": cache_hits,
        "cache_hit_rate": round(cache_hit_rate, 2),
        "avg_response_time_ms": round(avg_response_time, 2),
        "status_codes": {str(code): count for code, count in status_codes},
        "top_patents": [
            {"patent": p.patent_number, "requests": p.fetch_count}
            for p in top_patents
        ]
    }


@router.get("/stats/by-source")
async def get_stats_by_source(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to analyze")
):
    """Get statistics by data source (EPO, USPTO, Lens)."""
    
    # Count patents by source
    sources = db.query(
        PatentCache.source,
        func.count(PatentCache.id).label('count'),
        func.avg(func.extract('epoch', PatentCache.created_at - PatentCache.last_fetched) * 1000).label('avg_time')
    ).group_by(PatentCache.source).all()
    
    return {
        "sources": [
            {
                "source": s.source,
                "patent_count": s.count,
                "avg_fetch_time_ms": round(s.avg_time or 0, 2)
            }
            for s in sources
        ]
    }


@router.get("/stats/by-tier")
async def get_stats_by_tier(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to analyze")
):
    """Get usage statistics by user tier."""
    
    since = datetime.now() - timedelta(days=days)
    
    tiers = db.query(
        RequestLog.user_tier,
        func.count(RequestLog.id).label('requests'),
        func.count(func.distinct(RequestLog.api_key_hash)).label('unique_users')
    ).filter(
        RequestLog.created_at >= since
    ).group_by(RequestLog.user_tier).all()
    
    return {
        "tiers": [
            {
                "tier": t.user_tier,
                "total_requests": t.requests,
                "unique_users": t.unique_users
            }
            for t in tiers
        ]
    }


@router.get("/stats/timeline")
async def get_timeline_stats(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days to show")
):
    """Get daily request timeline."""
    
    since = datetime.now() - timedelta(days=days)
    
    # Requests per day
    daily_stats = db.query(
        func.date(RequestLog.created_at).label('date'),
        func.count(RequestLog.id).label('requests'),
        func.sum(func.cast(RequestLog.cache_hit, db.Integer)).label('cache_hits')
    ).filter(
        RequestLog.created_at >= since
    ).group_by(func.date(RequestLog.created_at)).order_by('date').all()
    
    return {
        "timeline": [
            {
                "date": str(stat.date),
                "requests": stat.requests,
                "cache_hits": stat.cache_hits or 0,
                "cache_hit_rate": round((stat.cache_hits or 0) / stat.requests * 100, 2)
            }
            for stat in daily_stats
        ]
    }