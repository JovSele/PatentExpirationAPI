"""
Unified Patent Service - Multi-source Orchestrator
Handles patent lookups with intelligent fallback across multiple sources.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.services.epo_service import EPOService
from app.services.lens_service import lens_service
from app.services.uspto_service import USPTOService
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class PatentService:
    """
    Unified patent service with multi-source fallback.
    
    Priority order:
    1. Cache (if fresh)
    2. Primary source (EPO for EP, USPTO for US)
    3. Lens.org (fallback)
    4. Secondary sources
    """
    
    def __init__(
        self,
        epo_service: EPOService,
        uspto_service: USPTOService,
        cache_service: CacheService
    ):
        self.epo = epo_service
        self.uspto = uspto_service
        self.lens = lens_service
        self.cache = cache_service
    
    async def get_patent_status(
        self, 
        db: Session, 
        patent_number: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get patent status with intelligent multi-source fallback.
        
        Args:
            db: Database session
            patent_number: Normalized patent number (e.g., EP1234567, US7654321)
            
        Returns:
            Dict with patent data or None if not found
        """
        # Normalize patent number
        patent_number = patent_number.strip().upper().replace(" ", "")
        
        # Log entry point
        logger.info(f"🔥 PATENT SERVICE CALLED FOR: {patent_number}")
        
        # Step 1: Check cache
        cached = self.cache.get_cached_patent(db, patent_number)
        if cached:
            logger.info(f"Cache HIT for {patent_number}")
            return {
                "patent_number": cached.patent_number,  
                "status": cached.status,
                "expiry_date": cached.expiry_date,
                "jurisdictions": cached.jurisdictions,
                "lapse_reason": cached.lapse_reason,
                "source": f"{cached.source} (cached)",
                "last_fetched": cached.last_fetched.isoformat(),  
                "cache_hit": True  # 
            }
        
        logger.info(f"Cache MISS for {patent_number} - fetching from sources")
        
        # Step 2: Try primary source based on patent prefix
        patent_data = None

        if patent_number.startswith("EP"):
            # European patent - try EPO first, then Lens
            patent_data = await self._try_epo(patent_number)

            # LENS FALLBACK - DISABLED (EPO je dostatočný)
            # if not patent_data:
            #     patent_data = await self._try_lens(patent_number)
                    
        elif patent_number.startswith("US"):
            # US patent - try USPTO first, then Lens
            patent_data = await self._try_uspto(patent_number)

            # LENS FALLBACK - DISABLED (EPO je dostatočný) 
            # if not patent_data:
            #     patent_data = await self._try_lens(patent_number)

        else:
            # Unknown jurisdiction - no fallback
            logger.warning(f"Unsupported jurisdiction for {patent_number}")
            patent_data = None

            # LENS FALLBACK - DISABLED
            # patent_data = await self._try_lens(patent_number)
        
        # Step 3: Save to cache if found
        if patent_data:
            cached = self.cache.save_patent_to_cache(db, patent_data)
            patent_data["cache_hit"] = False
            logger.info(f"Successfully fetched and cached {patent_number} from {patent_data.get('source')}")
            return patent_data
        
        # Step 4: Not found in any source
        logger.warning(f"Patent {patent_number} not found in any source")
        return None
    
    async def _try_epo(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """Try fetching from EPO API."""
        try:
            logger.info(f"Trying EPO for {patent_number}")
            data = await self.epo.get_patent_status(patent_number)
            if data:
                return self._normalize_response(data, "EPO")
            return None
        except Exception as e:
            logger.error(f"EPO error for {patent_number}: {str(e)}")
            return None
    
    async def _try_lens(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """Try fetching from Lens.org API."""
        try:
            logger.info(f"Trying Lens.org for {patent_number}")
            data = await self.lens.get_patent_status(patent_number)
            if data:
                return self._normalize_response(data, "Lens.org")
            return None
        except Exception as e:
            logger.error(f"Lens.org error for {patent_number}: {str(e)}")
            return None
    
    async def _try_uspto(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """Try fetching from USPTO API."""
        try:
            logger.info(f"Trying USPTO for {patent_number}")
            data = await self.uspto.get_patent_status(patent_number)
            if data:
                return self._normalize_response(data, "USPTO")
            return None
        except Exception as e:
            logger.error(f"USPTO error for {patent_number}: {str(e)}")
            return None
    
    def _normalize_response(
        self, 
        data: Dict[str, Any], 
        source: str
    ) -> Dict[str, Any]:
        """
        Normalize response from different sources to unified format.
        
        Expected output format:
        {
            "patent_number": str,
            "status": str,
            "expiry_date": str,
            "jurisdictions": dict,
            "lapse_reason": str,
            "source": str,
            "raw_data": dict
        }
        """
        # If data already has 'source' field, it's already normalized
        if "source" in data:
            return data
        
        # Otherwise, add source and ensure all required fields
        normalized = {
            "patent_number": data.get("patent_number", ""),
            "status": data.get("status", "Unknown"),
            "expiry_date": data.get("expiry_date"),
            "jurisdictions": data.get("jurisdictions", {}),
            "lapse_reason": data.get("lapse_reason"),
            "source": source,
            "raw_data": data
        }
        
        return normalized