"""
USPTO API integration.
Handles patent data retrieval from US Patent Office.
"""

import httpx
from typing import Dict, Any
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings


class USPTOService:
    """Service for interacting with USPTO API."""
    
    def __init__(self):
        self.base_url = settings.uspto_base_url
        self.api_key = settings.uspto_api_key
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_patent_status(self, patent_number: str) -> Dict[str, Any]:
        """
        Fetch patent status from USPTO API.
        
        Args:
            patent_number: US Patent number (e.g., US7654321)
            
        Returns:
            Dict with normalized patent data
        """
        # Extract numeric part from patent number
        # US7654321 -> 7654321
        patent_id = patent_number.replace("US", "").strip()
        
        # Construct API endpoint
        # Example: /patent/application?searchText=7654321
        endpoint = f"{self.base_url}/patent/application"
        
        params = {
            "searchText": patent_id
        }
        
        headers = {}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and normalize response
            return await self._parse_uspto_response(patent_number, data)
    
    async def _parse_uspto_response(
        self, 
        patent_number: str, 
        raw_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse USPTO API response into normalized format.
        
        USPTO API structure is different from EPO, need to extract:
        - Patent status
        - Expiry date
        - Maintenance fees status
        """
        # TODO: Implement proper USPTO response parsing
        # USPTO has different data structure than EPO
        
        # Placeholder implementation
        normalized = {
            "patent": patent_number,
            "status": "active",  # TODO: Parse from raw_data
            "expiry_date": None,  # TODO: Parse from raw_data
            "jurisdictions": ["US"],
            "lapse_reason": None,  # TODO: Check maintenance fees
            "source": "USPTO",
            "raw_data": raw_data,
            "last_update": datetime.now().isoformat()
        }
        
        return normalized
    
    async def check_maintenance_fees(self, patent_number: str) -> Dict[str, Any]:
        """
        Check maintenance fee status for US patents.
        Important for determining if patent has lapsed.
        """
        # TODO: Implement maintenance fee checking
        # US patents require maintenance fees at 3.5, 7.5, and 11.5 years
        
        return {
            "patent": patent_number,
            "fees_paid": True,  # Placeholder
            "next_due_date": None
        }
