"""
EPO Open Patent Services (OPS) API integration.
Handles OAuth2 authentication and patent data retrieval.
"""

import httpx
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings


class EPOService:
    """Service for interacting with EPO OPS API."""
    
    def __init__(self):
        self.base_url = settings.epo_base_url
        self.consumer_key = settings.epo_consumer_key
        self.consumer_secret = settings.epo_consumer_secret
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        
    def _get_auth_header(self) -> str:
        """Generate Basic Auth header for OAuth2."""
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    async def _get_access_token(self) -> str:
        """
        Get OAuth2 access token from EPO.
        Caches token until expiration.
        """
        # Return cached token if still valid
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Request new token
        url = "https://ops.epo.org/3.2/auth/accesstoken"
        headers = {
            "Authorization": self._get_auth_header(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            
            # Set expiration (subtract 60s buffer)
            expires_in = token_data.get("expires_in", 1200)  # Default 20 min
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
            
            return self.access_token
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_patent_status(self, patent_number: str) -> Dict[str, Any]:
        """
        Fetch patent status from EPO OPS API.
        
        Args:
            patent_number: Patent number (e.g., EP1234567)
            
        Returns:
            Dict with normalized patent data
        """
        # Get access token
        token = await self._get_access_token()
        
        # Construct API endpoint
        # Example: /rest-services/published-data/publication/epodoc/EP1234567
        endpoint = f"{self.base_url}/rest-services/published-data/publication/epodoc/{patent_number}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and normalize response
            return await self._parse_epo_response(patent_number, data)
    
    async def _parse_epo_response(
        self, 
        patent_number: str, 
        raw_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse EPO API response into normalized format.
        
        This is a simplified parser - real implementation needs to handle
        complex XML/JSON structures from EPO.
        """
        # TODO: Implement proper EPO response parsing
        # EPO returns complex nested structures, need to extract:
        # - Legal status
        # - Jurisdictions
        # - Expiry date
        # - Lapse reason
        
        # Placeholder implementation
        normalized = {
            "patent": patent_number,
            "status": "active",  # TODO: Parse from raw_data
            "expiry_date": None,  # TODO: Parse from raw_data
            "jurisdictions": ["EP"],  # TODO: Parse designated states
            "lapse_reason": None,
            "source": "EPO",
            "raw_data": raw_data,
            "last_update": datetime.now().isoformat()
        }
        
        return normalized
    
    async def get_legal_status(self, patent_number: str) -> Dict[str, Any]:
        """
        Fetch legal status events from EPO.
        
        Endpoint: /rest-services/legal
        """
        token = await self._get_access_token()
        
        endpoint = f"{self.base_url}/rest-services/legal/publication/epodoc/{patent_number}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            
            return response.json()
