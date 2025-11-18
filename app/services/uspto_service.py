"""
USPTO PatentsView API Integration
https://search.patentsview.org/
"""

import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)


class USPTOService:
    """Service for fetching patent data from USPTO PatentsView API."""
    
    def __init__(self):
        self.api_key = settings.uspto_api_key
        self.base_url = "https://search.patentsview.org/api/v1/patent/"
    
    async def get_patent_status(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """
        Fetch patent data from USPTO PatentsView API.
        
        Args:
            patent_number: US patent number (e.g., US7654321)
            
        Returns:
            Normalized patent data dict or None
        """
        try:
            # Remove US prefix
            clean_number = patent_number.replace("US", "").strip()
            
            # PatentsView API request body
            payload = {
                "q": {"patent_id": clean_number},
                "f": [
                    "patent_id",
                    "patent_date",
                    "patent_title",
                    "application"
                ],
                "o": {"size": 1}
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers={
                        "X-Api-Key": self.api_key,
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code != 200:
                    logger.warning(f"USPTO API {response.status_code}: {response.text[:300]}")
                    return None
                
                data = response.json()
                
                # Check for errors
                if data.get("error"):
                    logger.warning(f"USPTO API error for {patent_number}")
                    return None
                
                # Check if patent found
                patents = data.get("patents", [])
                if not patents:
                    logger.info(f"Patent {patent_number} not found in USPTO")
                    return None
                
                patent = patents[0]
                
                # Get filing date from application
                app_date = None
                application = patent.get("application", [])
                if application and len(application) > 0:
                    app_date = application[0].get("filing_date")
                
                # Calculate expiration (20 years from filing)
                expiry_date = None
                if app_date:
                    try:
                        filing_date = datetime.strptime(app_date, "%Y-%m-%d")
                        expiry_date = filing_date.replace(year=filing_date.year + 20).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
                
                return {
                    "patent_number": patent_number,
                    "status": "Granted",
                    "expiry_date": expiry_date,
                    "jurisdictions": {"primary": "US"},
                    "lapse_reason": None,
                    "source": "USPTO",
                    "raw_data": patent
                }
                
        except Exception as e:
            logger.error(f"USPTO error for {patent_number}: {str(e)}")
            return None


# Singleton instance
uspto_service = USPTOService()