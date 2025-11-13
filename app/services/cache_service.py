"""
Cache service for managing patent data in PostgreSQL.
Handles cache reads, writes, and TTL checks.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import PatentCache
from app.config import settings


class CacheService:
    """Service for managing patent cache."""
    
    @staticmethod
    def get_cached_patent(db: Session, patent_number: str) -> Optional[PatentCache]:
        """
        Get patent from cache if exists and not stale.
        
        Args:
            db: Database session
            patent_number: Patent number to lookup
            
        Returns:
            PatentCache object if found and fresh, None otherwise
        """
        cache_entry = db.query(PatentCache).filter(
            PatentCache.patent_number == patent_number
        ).first()
        
        if not cache_entry:
            return None
        
        # Check if cache is stale (older than TTL)
        ttl_threshold = datetime.now() - timedelta(days=settings.cache_ttl_days)
        
        if cache_entry.last_fetched < ttl_threshold:
            # Cache is stale, return None to trigger refresh
            return None
        
        # Update fetch count for popularity tracking
        cache_entry.fetch_count += 1
        db.commit()
        
        return cache_entry
    
    @staticmethod
    def save_patent_to_cache(
        db: Session, 
        patent_data: Dict[str, Any]
    ) -> PatentCache:
        """
        Save or update patent data in cache.
        
        Args:
            db: Database session
            patent_data: Normalized patent data dict
            
        Returns:
            PatentCache object
        """
        patent_number = patent_data["patent"]
        
        # Check if already exists
        cache_entry = db.query(PatentCache).filter(
            PatentCache.patent_number == patent_number
        ).first()
        
        if cache_entry:
            # Update existing entry
            cache_entry.status = patent_data.get("status")
            cache_entry.expiry_date = patent_data.get("expiry_date")
            cache_entry.jurisdictions = patent_data.get("jurisdictions")
            cache_entry.lapse_reason = patent_data.get("lapse_reason")
            cache_entry.source = patent_data.get("source")
            cache_entry.raw_data = patent_data.get("raw_data")
            cache_entry.last_fetched = datetime.now()
            cache_entry.updated_at = datetime.now()
            cache_entry.fetch_count += 1
        else:
            # Create new entry
            cache_entry = PatentCache(
                patent_number=patent_number,
                status=patent_data.get("status"),
                expiry_date=patent_data.get("expiry_date"),
                jurisdictions=patent_data.get("jurisdictions"),
                lapse_reason=patent_data.get("lapse_reason"),
                source=patent_data.get("source"),
                raw_data=patent_data.get("raw_data"),
                last_fetched=datetime.now(),
                fetch_count=1
            )
            db.add(cache_entry)
        
        db.commit()
        db.refresh(cache_entry)
        
        return cache_entry
    
    @staticmethod
    def get_top_requested_patents(db: Session, limit: int = 100) -> list[PatentCache]:
        """
        Get most frequently requested patents.
        Useful for prioritizing cache refresh.
        
        Args:
            db: Database session
            limit: Number of patents to return
            
        Returns:
            List of PatentCache objects
        """
        return db.query(PatentCache).order_by(
            PatentCache.fetch_count.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_stale_patents(db: Session, limit: int = 100) -> list[PatentCache]:
        """
        Get patents that need cache refresh (older than TTL).
        
        Args:
            db: Database session
            limit: Number of patents to return
            
        Returns:
            List of PatentCache objects
        """
        ttl_threshold = datetime.now() - timedelta(days=settings.cache_ttl_days)
        
        return db.query(PatentCache).filter(
            PatentCache.last_fetched < ttl_threshold
        ).order_by(
            PatentCache.fetch_count.desc()  # Prioritize popular patents
        ).limit(limit).all()
    
    @staticmethod
    def clear_cache(db: Session, patent_number: Optional[str] = None) -> int:
        """
        Clear cache for specific patent or all patents.
        
        Args:
            db: Database session
            patent_number: Specific patent to clear, None for all
            
        Returns:
            Number of entries deleted
        """
        if patent_number:
            count = db.query(PatentCache).filter(
                PatentCache.patent_number == patent_number
            ).delete()
        else:
            count = db.query(PatentCache).delete()
        
        db.commit()
        return count
