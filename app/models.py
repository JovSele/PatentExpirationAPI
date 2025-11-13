"""
SQLAlchemy database models.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Index
from sqlalchemy.sql import func
from app.database import Base


class PatentCache(Base):
    """
    Stores cached patent status information.
    TTL: 30 days (configurable)
    """
    __tablename__ = "patent_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    patent_number = Column(String, unique=True, index=True, nullable=False)
    
    # Patent information
    status = Column(String, nullable=False)  # "active" or "expired"
    expiry_date = Column(String, nullable=True)
    jurisdictions = Column(JSON, nullable=True)  # ["EP", "DE", "FR"]
    lapse_reason = Column(String, nullable=True)
    source = Column(String, nullable=False)  # "EPO" or "USPTO"
    
    # Raw response data (for debugging)
    raw_data = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    last_fetched = Column(DateTime(timezone=True), server_default=func.now())
    fetch_count = Column(Integer, default=1)  # Track popularity
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_patent_status', 'patent_number', 'status'),
        Index('idx_last_fetched', 'last_fetched'),
        Index('idx_fetch_count', 'fetch_count'),
    )


class RequestLog(Base):
    """
    Logs API requests for analytics and rate limiting.
    """
    __tablename__ = "request_log"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Request details
    patent_number = Column(String, index=True, nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    
    # User/API key tracking (from RapidAPI headers)
    api_key_hash = Column(String, index=True, nullable=True)
    user_tier = Column(String, nullable=True)  # "free", "basic", "pro"
    
    # Response details
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    cache_hit = Column(Boolean, default=False)
    
    # IP and headers (optional, for abuse detection)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_api_key_date', 'api_key_hash', 'created_at'),
        Index('idx_created_at', 'created_at'),
    )
