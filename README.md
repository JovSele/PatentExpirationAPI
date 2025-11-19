# 📋 Patent Expiration API

**B2B Micro-Service API** for checking patent status (active/expired) and jurisdictions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)

---

## 🎯 What does this API do?

Simple answers to 3 questions:
1. **Is the patent active?** → `"status": "Granted"` or `"Expired"`
2. **Where is it active?** → `"jurisdictions": {"primary": "EP"}`
3. **When does it expire?** → `"expiry_date": "2028-05-15"`

**Supported jurisdictions:** EPO (European patents), USPTO (US patents)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (or Docker)
- Git

### 1. Clone & Install
```bash
# Clone repository
git clone https://github.com/your-username/patent-expiration-api.git
cd patent-expiration-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys:
# - EPO_CONSUMER_KEY
# - EPO_CONSUMER_SECRET
# - USPTO_API_KEY
# - DATABASE_URL
# - SECRET_KEY
```

### 3. Database Setup
```bash
# Run migrations
alembic upgrade head
```

### 4. Run Development Server
```bash
# Start API server
uvicorn app.main:app --reload

# API available at: http://localhost:8000
# Documentation: http://localhost:8000/docs
```

---

## 📖 API Usage

### Single Patent Lookup

**Request:**
```bash
GET /api/v1/status?patent=EP1234567
```

**Response:**
```json
{
  "patent_number": "EP1234567",
  "status": "Granted",
  "expiry_date": "2021-11-04",
  "jurisdictions": {"primary": "EP"},
  "lapse_reason": null,
  "source": "EPO",
  "last_fetched": "2025-11-11T10:30:00Z",
  "cache_hit": false
}
```

### Health Check
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-18T12:00:00Z",
  "database": "connected"
}
```

### Analytics Dashboard

**Overview Stats:**
```bash
GET /api/v1/stats/overview?days=30
```

**Response:**
```json
{
  "period_days": 30,
  "total_requests": 1523,
  "cache_hit_rate": 78.5,
  "avg_response_time_ms": 245.3,
  "status_codes": {"200": 1480, "404": 43},
  "top_patents": [
    {"patent": "EP3000000", "requests": 89}
  ]
}
```

**Stats by Source:**
```bash
GET /api/v1/stats/by-source
```

**Stats by Tier:**
```bash
GET /api/v1/stats/by-tier
```

**Daily Timeline:**
```bash
GET /api/v1/stats/timeline?days=7
```

---

## 🐳 Docker Deployment

### Local Development
```bash
# Build & run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
```

### Production (Render.com)

1. Push to GitHub
2. Connect Render.com to your repository
3. Add environment variables in Render dashboard
4. Deploy! 🚀

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 🧪 Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_endpoints.py
```

---

## 📊 Pricing & Rate Limits

| Tier            | Monthly Price | Requests/Month | Price per Request | Overage Fee* |
|-----------------|---------------|----------------|-------------------|--------------|
| **Free**        | €0            | 20             | N/A               | N/A          |
| **Starter**     | €19           | 1,000          | €0.019            | €0.030       |
| **Pro**         | €99           | 10,000         | €0.0099           | €0.015       |
| **Enterprise**  | Custom        | Custom         | Contact us        | Custom       |

*Overage Fee = price per request above monthly limit

### Rate Limit Headers

All responses include rate limit information:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 856
X-RateLimit-Reset: 2025-12-18T12:00:00Z
```

---

## 🔒 Legal Disclaimer

⚠️ **IMPORTANT:** This API provides patent status information **for informational purposes only**.

- **NOT legal advice**
- **NOT a substitute for professional patent attorney consultation**
- Data accuracy depends on external sources (EPO, USPTO)
- No warranty or guarantee of accuracy

**Use at your own risk.** Always verify critical patent information with official patent offices:
- **EPO:** https://www.epo.org
- **USPTO:** https://www.uspto.gov

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 14+
- **Caching:** 30-day intelligent cache
- **APIs:** EPO OPS (free), USPTO PatentsView (free)
- **Hosting:** Render.com / Railway / Fly.io
- **Marketplace:** RapidAPI Hub

### Key Features

✅ Multi-source patent data (EPO, USPTO)  
✅ Intelligent 30-day caching (sub-second responses)  
✅ Tiered rate limiting with API key support  
✅ Analytics dashboard  
✅ Comprehensive error handling  
✅ OpenAPI/Swagger documentation  

---

## 📁 Project Structure
```
patent-expiration-api/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration & settings
│   ├── models.py                    # Database models (SQLAlchemy)
│   ├── schemas.py                   # Pydantic schemas
│   ├── database.py                  # Database connection
│   ├── exceptions.py                # Custom exceptions
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints.py         # Patent status endpoints
│   │       ├── analytics.py         # Analytics endpoints
│   │       └── dependencies.py      # Dependency injection
│   ├── services/
│   │   ├── epo_service.py           # EPO OPS integration
│   │   ├── uspto_service.py         # USPTO PatentsView integration
│   │   ├── patent_service.py        # Multi-source orchestration
│   │   └── cache_service.py         # Caching logic
│   ├── middleware/
│   │   └── advanced_rate_limiter.py # Rate limiting
│   └── utils/
│       ├── rate_limiter.py          # Rate limit utilities
│       └── normalizer.py            # Data normalization
├── tests/
│   ├── test_endpoints.py            # API endpoint tests
│   └── test_services.py             # Service layer tests
├── alembic/                         # Database migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Environment Variables

Required environment variables (see `.env.example`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/patent_db

# EPO OPS API (free)
EPO_CONSUMER_KEY=your_epo_key
EPO_CONSUMER_SECRET=your_epo_secret

# USPTO PatentsView API (free)
USPTO_API_KEY=your_uspto_key

# Security
SECRET_KEY=your_random_secret_key

# Optional
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🐛 Issues & Support

- **GitHub Issues:** [Report a bug](https://github.com/your-username/patent-expiration-api/issues)
- **Email:** support@patentapi.com
- **RapidAPI Support:** Use RapidAPI messaging system

---

## 🚦 API Status

- **Production:** https://patent-api.onrender.com
- **Status Page:** https://status.patentapi.com
- **Documentation:** https://patent-api.onrender.com/docs

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Jov Sele

---

## 🙏 Acknowledgments

- [EPO Open Patent Services (OPS)](https://www.epo.org/searching-for-patents/data/web-services/ops.html)
- [USPTO PatentsView API](https://search.patentsview.org/)
- [FastAPI Framework](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Made with ❤️ by [Jov Sele](https://github.com/jovsele)**