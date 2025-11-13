# Patent Expiration API - Development Plan

**Projekt:** B2B Micro-Service API pre overenie statusu patentov  
**Hosting:** Render.com (free tier)  
**Monetizácia:** RapidAPI (credit-based)  
**Status:** 🚧 In Development

---

## 🎯 MVP Ciele

**Core Value Proposition:**
Jednoduchá REST API odpoveď na otázku: "Je tento patent aktívny a kde?"

**Must-Have Features:**
- Single patent lookup (batch v2)
- EPO + USPTO patenty
- Status: active/expired
- Expiry date
- Jurisdikcie (EP, US, JP, CN)
- Lapse reason (fee not paid, withdrawal, etc.)
- Rate limiting (podľa RapidAPI tiers)
- Legal disclaimers

---

## ✅ Development Checklist

### Phase 1: Project Setup & Infrastructure
- [x] 1.1 Vytvorenie štruktúry projektu
- [x] 1.2 Git inicializácia + .gitignore
- [x] 1.3 Requirements.txt (FastAPI, SQLAlchemy, httpx, etc.)
- [x] 1.4 .env.example (API keys, DB config)
- [x] 1.5 Docker setup (Dockerfile, docker-compose.yml)
- [x] 1.6 README.md (setup instructions)

### Phase 2: Database & Models
- [x] 2.1 Database schema design
- [x] 2.2 SQLAlchemy models (PatentCache, RequestLog)
- [x] 2.3 Pydantic schemas (request/response)
- [x] 2.4 Database migrations (Alembic)
- [x] 2.5 Connection pooling & config

### Phase 3: External API Integrations
- [x] 3.1 EPO OPS API client
  - [x] OAuth2 authentication
  - [x] Rate limit handling (personal: ~1000/week)
  - [x] Error handling & retries
- [x] 3.2 USPTO API client
  - [x] Patent search endpoint
  - [x] Data parsing
  - [x] Error handling
- [x] 3.3 Data normalizer (unified JSON format)
- [x] 3.4 Response caching logic (30-day TTL)

### Phase 4: Core API Endpoints
- [x] 4.1 FastAPI app setup (main.py)
- [x] 4.2 Health check endpoint (`/health`)
- [x] 4.3 Patent status endpoint (`/api/v1/status?patent=EP1234567`)
  - [x] Input validation
  - [x] Cache check (Postgres)
  - [x] Fetch from EPO/USPTO if needed
  - [x] Normalize response
  - [x] Store in cache
- [x] 4.4 API versioning (v1)
- [x] 4.5 CORS configuration (for RapidAPI)

### Phase 5: Rate Limiting & Security
- [x] 5.1 Rate limiter middleware
  - [x] Free tier: 20 requests/month
  - [x] Basic: 1000 requests/month
  - [x] Pro: 10000 requests/month
- [x] 5.2 API key validation (RapidAPI headers)
- [x] 5.3 Request logging (analytics)
- [x] 5.4 Security headers (helmet.js equivalent)

### Phase 6: Legal & Documentation
- [x] 6.1 Legal disclaimer (liability protection)
- [x] 6.2 Warranty disclaimer ("informational purposes only")
- [x] 6.3 Terms of Service
- [x] 6.4 API documentation (OpenAPI/Swagger)
- [ ] 6.5 RapidAPI description page

### Phase 7: Testing
- [x] 7.1 Unit tests (services, normalizer)
- [x] 7.2 Integration tests (API endpoints)
- [ ] 7.3 Mock EPO/USPTO responses
- [ ] 7.4 Cache behavior tests
- [ ] 7.5 Rate limiting tests

### Phase 8: Deployment
- [ ] 8.1 Render.yaml configuration
- [ ] 8.2 Environment variables setup
- [ ] 8.3 PostgreSQL provisioning (Render)
- [ ] 8.4 Deploy to Render.com
- [ ] 8.5 Health checks & monitoring
- [ ] 8.6 RapidAPI integration
  - [ ] API upload
  - [ ] Pricing tiers
  - [ ] Testing on RapidAPI

### Phase 9: Post-Launch
- [ ] 9.1 Monitoring setup (logs, errors)
- [ ] 9.2 Performance optimization
- [ ] 9.3 User feedback collection
- [ ] 9.4 Bug fixes
- [ ] 9.5 Documentation updates

---

## 🔧 Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (async REST API)
- SQLAlchemy (ORM)
- PostgreSQL (cache storage)
- httpx (async HTTP client)
- Pydantic (validation)

**Deployment:**
- Docker
- Render.com (free tier)
- RapidAPI (marketplace)

**Skipped for MVP:**
- ~~Redis~~ (PostgreSQL cache je OK)
- ~~Celery~~ (direct API calls)
- ~~Batch API~~ (v2)
- ~~Auto-refresh jobs~~ (on-demand refresh)

---

## 📊 Unified Response Format

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

---

## 🚀 Success Metrics

**Technical:**
- Response time: < 2s (cache hit: < 200ms)
- Uptime: > 99%
- Error rate: < 1%

**Business:**
- 10 API users v prvých 30 dňoch
- 100+ API calls/mesiac
- Conversion: free → paid tier > 5%

---

## 📝 Notes

- EPO OPS: Personal license (~1000 requests/week)
- USPTO: Free public API
- Cache TTL: 30 days (stale data = re-fetch)
- Top requested patents: refresh prioritne
- Legal protection: strong disclaimers

---

**Last Updated:** 2025-11-13  
**Version:** 1.0-MVP
