# Changelog

All notable changes to Patent Expiration API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Batch patent lookup endpoint
- Webhook notifications for patent expiry
- Historical patent data analysis

---

## [1.0.0] - 2025-11-18

### 🎉 Initial Release

#### Added
- **Core Features**
  - Single patent status lookup (EP, US)
  - Multi-source data aggregation (EPO OPS, USPTO PatentsView)
  - Intelligent 30-day caching system
  - PostgreSQL database with SQLAlchemy ORM
  
- **API Endpoints**
  - `GET /api/v1/status` - Patent status lookup
  - `GET /api/v1/health` - Health check
  - `GET /api/v1/stats/overview` - Usage statistics
  - `GET /api/v1/stats/by-source` - Stats by data source
  - `GET /api/v1/stats/by-tier` - Stats by user tier
  - `GET /api/v1/stats/timeline` - Daily timeline

- **Rate Limiting**
  - Tiered rate limits (Free: 20, Starter: 1000, Pro: 10000 req/month)
  - Per-API-key tracking
  - Rate limit headers in responses
  - Monthly reset cycle

- **Error Handling**
  - Custom exception classes
  - Structured error responses
  - Proper HTTP status codes (400, 404, 429, 500)
  - Comprehensive logging

- **Analytics**
  - Request logging with detailed metrics
  - Cache hit rate tracking
  - Response time monitoring
  - Source distribution analysis

- **Documentation**
  - OpenAPI/Swagger documentation at `/docs`
  - ReDoc documentation at `/redoc`
  - Comprehensive README.md
  - Environment setup guide (.env.example)

- **Data Sources**
  - EPO OPS API integration (OAuth2)
  - USPTO PatentsView API integration
  - Lens.org API support (disabled by default)

- **Development Tools**
  - Docker & Docker Compose setup
  - Alembic migrations
  - pytest test suite
  - Code quality tools (black, flake8, mypy)

#### Technical Stack
- FastAPI 0.109.0
- Python 3.11+
- PostgreSQL 14+
- SQLAlchemy 2.0
- Pydantic 2.5
- httpx for async HTTP requests

#### Deployment
- Render.com configuration (render.yaml)
- Docker containerization
- Environment-based configuration
- Production-ready error handling

---

## Version Numbering

- **Major (X.0.0)**: Breaking changes, major new features
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, minor improvements

---

## Links

- [GitHub Repository](https://github.com/JovSele/PatentExpirationAPI)
- [Documentation](https://patent-api.onrender.com/docs)
- [RapidAPI Listing](https://rapidapi.com/your-api)