"""
Data normalizer utility.
Unifies patent data from different sources (EPO, USPTO) into consistent format.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


class PatentNormalizer:
    """Normalizes patent data from different sources into unified format."""
    
    @staticmethod
    def normalize(
        patent_number: str,
        source: str,
        raw_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Normalize patent data based on source.
        
        Args:
            patent_number: Patent number
            source: Data source ("EPO" or "USPTO")
            raw_data: Raw API response data
            
        Returns:
            Normalized patent data dict
        """
        if source == "EPO":
            return PatentNormalizer._normalize_epo(patent_number, raw_data)
        elif source == "USPTO":
            return PatentNormalizer._normalize_uspto(patent_number, raw_data)
        else:
            raise ValueError(f"Unknown source: {source}")
    
    @staticmethod
    def _normalize_epo(patent_number: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize EPO OPS API response.
        
        EPO structure (simplified):
        - ops:world-patent-data
          - exchange-documents
            - exchange-document
              - bibliographic-data
                - publication-reference
                - application-reference
        """
        # TODO: Implement proper EPO XML/JSON parsing
        # This is placeholder implementation
        
        status = "active"
        expiry_date = None
        jurisdictions = ["EP"]
        lapse_reason = None
        
        # Try to extract data from raw_data
        # Real implementation needs to navigate complex nested structure
        
        return {
            "patent": patent_number,
            "status": status,
            "expiry_date": expiry_date,
            "jurisdictions": jurisdictions,
            "lapse_reason": lapse_reason,
            "source": "EPO",
            "raw_data": raw_data,
            "last_update": datetime.now().isoformat()
        }
    
    @staticmethod
    def _normalize_uspto(patent_number: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize USPTO API response.
        
        USPTO structure:
        - results: []
          - patentNumber
          - patentStatus
          - filingDate
          - publicationDate
        """
        # TODO: Implement proper USPTO parsing
        # This is placeholder implementation
        
        status = "active"
        expiry_date = None
        jurisdictions = ["US"]
        lapse_reason = None
        
        # Try to extract from results
        if "results" in raw_data and len(raw_data["results"]) > 0:
            result = raw_data["results"][0]
            
            # Parse status
            patent_status = result.get("patentStatus", "").lower()
            if "expired" in patent_status or "abandoned" in patent_status:
                status = "expired"
                lapse_reason = patent_status
        
        return {
            "patent": patent_number,
            "status": status,
            "expiry_date": expiry_date,
            "jurisdictions": jurisdictions,
            "lapse_reason": lapse_reason,
            "source": "USPTO",
            "raw_data": raw_data,
            "last_update": datetime.now().isoformat()
        }
    
    @staticmethod
    def calculate_expiry_date(
        filing_date: str,
        patent_type: str = "utility"
    ) -> Optional[str]:
        """
        Calculate patent expiry date.
        
        Rules:
        - Utility patents: 20 years from filing date
        - Design patents: 15 years from grant date (US), 25 years (EU)
        
        Args:
            filing_date: Filing date (ISO format)
            patent_type: "utility" or "design"
            
        Returns:
            Expiry date (ISO format) or None
        """
        try:
            from dateutil.parser import parse
            from dateutil.relativedelta import relativedelta
            
            filing = parse(filing_date)
            
            if patent_type == "utility":
                expiry = filing + relativedelta(years=20)
            elif patent_type == "design":
                expiry = filing + relativedelta(years=15)
            else:
                return None
            
            return expiry.date().isoformat()
        except Exception:
            return None
    
    @staticmethod
    def parse_jurisdictions(designated_states: List[str]) -> List[str]:
        """
        Parse and normalize jurisdiction codes.
        
        Args:
            designated_states: List of country/region codes
            
        Returns:
            Normalized list of jurisdictions
        """
        # Map common variants to standard codes
        jurisdiction_map = {
            "EPO": "EP",
            "EUROPEAN PATENT OFFICE": "EP",
            "UNITED STATES": "US",
            "USA": "US",
            "DEUTSCHLAND": "DE",
            "GERMANY": "DE",
            "FRANCE": "FR",
            "FRANKREICH": "FR",
        }
        
        normalized = []
        for state in designated_states:
            state_upper = state.upper()
            normalized_state = jurisdiction_map.get(state_upper, state_upper)
            
            if normalized_state not in normalized:
                normalized.append(normalized_state)
        
        return normalized
