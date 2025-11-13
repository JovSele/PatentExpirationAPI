# 📋 Patent Expiration API

**B2B Micro-Service API** pre overenie statusu patentov (aktívny/expirovaný) a jurisdikcií.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)

---

## 🎯 Čo táto API robí?

Jednoduchá odpoveď na 3 otázky:
1. **Je patent aktívny?** → `"status": "active"` alebo `"expired"`
2. **Kde je aktívny?** → `"jurisdictions": ["EP", "DE", "FR"]`
3. **Kedy expiruje?** → `"expiry_date": "2028-05-15"`

**Podporované jurisdikcie:** EPO (európske patenty), USPTO (US patenty)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (alebo Docker)
- Git

### 1. Clone & Install

```bash
# Clone repository
git clone https://github.com/your-username/patent-expiration-api.git
cd patent-expiration-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# alebo: venv\Scripts\activate  # Windows

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
# - USPTO_API_KEY (optional)
# - DATABASE_URL
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

# API dostupné na: http://localhost:8000
# Dokumentácia: http://localhost:8000/docs
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
  "patent": "EP1234567",
  "status": "expired",
  "expiry_date": "2021-11-04",
  "jurisdictions": ["EP", "DE", "FR"],
  "lapse_reason": "fee not paid",
  "source": "EPO",
  "last_update": "2025-11-11T10:30:00Z",
  "disclaimer": "For informational purposes only. Not legal advice."
}
```

### Health Check

```bash
GET /health
```

---

## 🐳 Docker Deployment

### Local Development

```bash
# Build & run with Docker Compose
docker-compose up --build

# API bude dostupné na http://localhost:8000
```

### Production (Render.com)

1. Push to GitHub
2. Connect Render.com to repository
3. Add environment variables v Render dashboard
4. Deploy! 🚀

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

## 📊 Rate Limits (RapidAPI Tiers)

| Tier       | Requests/Month | Price      |
|------------|----------------|------------|
| **Free**   | 20             | €0         |
| **Basic**  | 1,000          | €19/month  |
| **Pro**    | 10,000         | €99/month  |
| **Enterprise** | Custom     | Contact us |

---

## 🔒 Legal Disclaimer

⚠️ **IMPORTANT:** This API provides patent status information **for informational purposes only**. 

- **NOT legal advice**
- **NOT a substitute for professional patent attorney consultation**
- Data accuracy depends on external sources (EPO, USPTO)
- No warranty or guarantee of accuracy

**Use at your own risk.** Always verify critical patent information with official patent offices.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **Hosting:** Render.com (free tier)
- **APIs:** EPO OPS, USPTO
- **Marketplace:** RapidAPI

---

## 📁 Project Structure

```
patent-expiration-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints.py # API routes
│   │       └── dependencies.py
│   ├── services/
│   │   ├── epo_service.py   # EPO integration
│   │   ├── uspto_service.py # USPTO integration
│   │   └── cache_service.py
│   └── utils/
│       ├── rate_limiter.py
│       └── normalizer.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── PLAN.md
```

---

## 🐛 Issues & Support

- **GitHub Issues:** [Report bug](https://github.com/your-username/patent-expiration-api/issues)
- **Email:** support@yourservice.com
- **RapidAPI Support:** Use RapidAPI messaging

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- EPO Open Patent Services (OPS)
- USPTO Developer Portal
- FastAPI & Pydantic communities

---

**Made with ❤️ by [Your Name]**
