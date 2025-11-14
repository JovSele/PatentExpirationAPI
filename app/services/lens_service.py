"""
Lens.org Patent API Service
Provides patent legal status and expiration data from Lens.org
"""

import httpx
from typing import Dict, Optional, Any
from datetime import datetime
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class LensService:
    """Service for interacting with Lens.org Patent API."""
    
    def __init__(self):
        self.base_url = settings.lens_base_url
        self.api_token = settings.lens_api_token
        self.rate_limit = settings.lens_rate_limit_per_minute
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def get_patent_status(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """
        Fetch patent legal status from Lens.org
        
        Args:
            patent_number: Patent number (e.g., EP1234567, US1234567)
            
        Returns:
            Dict with patent status data or None if not found
        """
        try:
            # Normalize patent number for Lens query
            normalized = self._normalize_patent_number(patent_number)
            
           # Lens.org query payload - používaj pole 'ids'
            query = {
                "query": {
                    "match": {
                        "ids": normalized
                    }
                },
                "include": [
                    "lens_id",
                    "doc_number",
                    "jurisdiction",
                    "kind",
                    "date_published",
                    "legal_status"
                ],
                "size": 1
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:

                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=query
                )
                

                if response.status_code == 200:
                    data = response.json()
                    return self._parse_lens_response(data, patent_number)
                elif response.status_code == 401:
                    logger.error("Lens.org authentication failed - check API token")
                    return None
                elif response.status_code == 429:
                    logger.warning("Lens.org rate limit exceeded")
                    return None
                else:
                    logger.error(f"Lens.org API error: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching patent {patent_number} from Lens.org")
            return None
        except Exception as e:
            logger.error(f"Error fetching from Lens.org: {str(e)}")
            return None
    
    def _normalize_patent_number(self, patent_number: str) -> str:
        """
        Normalize patent number for Lens.org query.
        Lens typically expects format like: EP1234567A1, US1234567B2
        """
        # Remove spaces and convert to uppercase
        normalized = patent_number.replace(" ", "").upper()
        return normalized
    
    def _parse_lens_response(self, data: Dict, original_patent: str) -> Optional[Dict[str, Any]]:
        """Parse Lens.org API response into standardized format."""
        try:
            if data.get("total", 0) == 0:
                logger.info(f"Patent {original_patent} not found in Lens.org")
                return None
            
            # Get first result
            patent_data = data.get("data", [])[0]
            
            # Extract legal status
            legal_status = patent_data.get("legal_status", {})
            
            # Determine current status
            current_status = "Unknown"
            if legal_status.get("granted"):
                current_status = "Granted"
            elif legal_status.get("patent_status"):
                current_status = legal_status["patent_status"].capitalize()
            
            # Get expiration date
            expiry_date = legal_status.get("anticipated_term_date") or legal_status.get("discontinuation_date")
            
            # Build standardized response
            result = {
                "patent_number": original_patent,
                "status": current_status,
                "expiry_date": expiry_date,
                "jurisdictions": {"primary": patent_data.get("jurisdiction")},
                "lapse_reason": None,
                "source": "lens.org",
                "raw_data": patent_data
            }
            
            logger.info(f"Successfully fetched patent {original_patent} from Lens.org")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing Lens.org response: {str(e)}")
            return None
    
    async def search_patents(self, query: str, size: int = 10) -> Dict[str, Any]:
        """
        Search patents using Lens.org query syntax.
        
        Args:
            query: Lens.org query string
            size: Number of results (max 100 on trial)
            
        Returns:
            Dict with search results
        """
        try:
            payload = {
                "query": query,
                "size": min(size, 100),  # Trial limit
                "include": [
                    "lens_id",
                    "publication_number",
                    "title",
                    "legal_status",
                    "expiration_date"
                ]
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Lens search error: {response.status_code}")
                    return {"total": 0, "data": []}
                    
        except Exception as e:
            logger.error(f"Error in Lens.org search: {str(e)}")
            return {"total": 0, "data": []}


# Global instance
lens_service = LensService()