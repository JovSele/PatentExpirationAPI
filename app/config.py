"""
Application configuration using Pydantic Settings.
Loads configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Patent Expiration API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Database
    database_url: str
    
    # EPO OPS API
    epo_consumer_key: str
    epo_consumer_secret: str
    epo_base_url: str = "https://ops.epo.org/3.2"

    # Lens.org Patent API
    lens_api_token: str
    lens_base_url: str = "https://api.lens.org/patent/search"
    lens_rate_limit_per_minute: int = 10
    
    # USPTO API
    uspto_api_key: str = ""
    uspto_base_url: str = "https://developer.uspto.gov/ds-api"
    
    # Cache Settings
    cache_ttl_days: int = 30
    cache_refresh_top_n: int = 100
    
    # Rate Limiting (requests per month)
    rate_limit_free: int = 20
    rate_limit_basic: int = 1000
    rate_limit_pro: int = 10000
    
    # RapidAPI
    rapidapi_proxy_secret: str = ""
    rapidapi_header_name: str = "X-RapidAPI-Proxy-Secret"
    
    # Security
    secret_key: str
    allowed_hosts: str = "*"
    cors_origins: List[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # External Services
    request_timeout: int = 30
    max_retries: int = 3
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()