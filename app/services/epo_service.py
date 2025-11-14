"""
EPO OPS (Open Patent Services) Integration
OAuth2 authentication + patent data fetching
"""

import httpx
import base64
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config import settings

logger = logging.getLogger(__name__)


class EPOService:
    """Service for fetching patent data from EPO OPS API."""
    
    def __init__(self):
        self.consumer_key = settings.epo_consumer_key
        self.consumer_secret = settings.epo_consumer_secret
        self.base_url = "https://ops.epo.org/3.2"
        self.token = None
        self.token_expiry = None
    
    async def _get_token(self) -> str:
        """Get OAuth2 access token from EPO."""
        # Check if existing token is still valid
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token
        
        # Get new token
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        auth = base64.b64encode(credentials.encode()).decode()
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.post(
                f"{self.base_url}/auth/accesstoken",
                headers={
                    "Authorization": f"Basic {auth}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"grant_type": "client_credentials"}
            )
            
            if response.status_code != 200:
                raise Exception(f"EPO auth failed: {response.status_code}")
            
            token_data = response.json()
            self.token = token_data["access_token"]
            # Token expires in ~20 minutes, cache for 15 min to be safe
            self.token_expiry = datetime.now() + timedelta(minutes=15)
            
            logger.info("EPO OAuth2 token obtained")
            return self.token
    
    async def get_patent_status(self, patent_number: str) -> Optional[Dict[str, Any]]:
        """
        Fetch patent data from EPO OPS.
        
        Args:
            patent_number: Patent number (e.g., EP0683520)
            
        Returns:
            Normalized patent data dict or None
        """
        try:
            token = await self._get_token()
            
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                response = await client.get(
                    f"{self.base_url}/rest-services/published-data/publication/epodoc/{patent_number}",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/json"
                    }
                )
                
                if response.status_code != 200:
                    logger.warning(f"EPO API returned {response.status_code} for {patent_number}")
                    return None
                
                data = response.json()
                
                # Extract dates and calculate expiration
                dates = self._extract_dates(data)
                expiry_date = self._calculate_expiration(dates['application_date'])
                
                # Determine status
                status = "Granted" if dates['grant_date'] != 'N/A' else "Pending"
                
                return {
                    "patent_number": patent_number,
                    "status": status,
                    "expiry_date": expiry_date,
                    "jurisdictions": {"primary": "EP"},
                    "lapse_reason": None,
                    "source": "EPO",
                    "raw_data": {
                        "application_date": dates['application_date'],
                        "grant_date": dates['grant_date']
                    }
                }
                
        except Exception as e:
            logger.error(f"EPO error for {patent_number}: {str(e)}")
            return None
    
    def _extract_dates(self, data: dict) -> dict:
        """Extract application and grant dates from EPO JSON response."""
        application_date = 'N/A'
        grant_date = 'N/A'
        
        # Navigate to exchange documents
        exchange_documents = data.get('ops:world-patent-data', {}).get('exchange-documents', {}).get('exchange-document', [])
        
        # Handle single document (dict) vs multiple (list)
        if isinstance(exchange_documents, dict):
            exchange_documents = [exchange_documents]
        elif not isinstance(exchange_documents, list):
            return {'application_date': 'N/A', 'grant_date': 'N/A'}
        
        # 1. Find Application Date
        for doc in exchange_documents:
            app_ref = doc.get('bibliographic-data', {}).get('application-reference', {})
            for doc_id in app_ref.get('document-id', []):
                if doc_id.get('@document-id-type') == 'epodoc':
                    date_element = doc_id.get('date', {})
                    if date_element and date_element.get('$'):
                        application_date = date_element['$']
                        break
            if application_date != 'N/A':
                break
        
        # 2. Find Grant Date (publication date of B1/B2/B3 document)
        for doc in exchange_documents:
            kind = doc.get('@kind', '')
            # Hľadaj B dokumenty (B1, B2, B3 = granted patents)
            if kind and kind.startswith('B'):
                pub_ref = doc.get('bibliographic-data', {}).get('publication-reference', {})
                doc_ids = pub_ref.get('document-id', [])
                
                # Handle single doc_id (dict) vs multiple (list)
                if isinstance(doc_ids, dict):
                    doc_ids = [doc_ids]
                
                for doc_id in doc_ids:
                    date_element = doc_id.get('date', {})
                    if isinstance(date_element, dict) and date_element.get('$'):
                        grant_date = date_element['$']
                        logger.info(f"Found grant date: {grant_date} in document kind: {kind}")
                        break
                    elif isinstance(date_element, str):
                        grant_date = date_element
                        logger.info(f"Found grant date: {grant_date} in document kind: {kind}")
                        break
                
                if grant_date != 'N/A':
                    break
        
        return {
            'application_date': application_date,
            'grant_date': grant_date
        }
    
    def _calculate_expiration(self, app_date_str: str) -> Optional[str]:
        """Calculate theoretical expiration (20 years from filing)."""
        if app_date_str == 'N/A':
            return None
        
        try:
            # Convert YYYYMMDD to datetime
            app_date = datetime.strptime(app_date_str, '%Y%m%d')
            # Add 20 years
            expiration_date = app_date.replace(year=app_date.year + 20)
            return expiration_date.strftime('%Y-%m-%d')
        except ValueError:
            return None


# Singleton instance
epo_service = EPOService()