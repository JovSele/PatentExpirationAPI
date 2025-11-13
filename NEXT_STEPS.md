# 📋 Next Steps & TODO

## ✅ Čo je HOTOVÉ (MVP Foundation)

### Infrastructure ✓
- ✅ Complete project structure
- ✅ Docker setup (docker-compose.yml)
- ✅ FastAPI application with middleware
- ✅ PostgreSQL models & migrations (Alembic)
- ✅ Render.com deployment config
- ✅ Environment configuration (.env.example)

### Core Features ✓
- ✅ `/api/v1/status` endpoint (patent lookup)
- ✅ `/api/v1/health` endpoint
- ✅ Rate limiting middleware (RapidAPI tiers)
- ✅ Request logging & analytics
- ✅ Cache system (30-day TTL)
- ✅ Legal disclaimers

### Services ✓
- ✅ EPO service skeleton (OAuth2 auth)
- ✅ USPTO service skeleton
- ✅ Cache service (PostgreSQL)
- ✅ Data normalizer
- ✅ Rate limiter

### Documentation ✓
- ✅ README.md
- ✅ DEPLOYMENT.md
- ✅ COMMANDS.md
- ✅ PLAN.md
- ✅ OpenAPI docs (FastAPI auto-generated)

---

## 🚧 Čo TREBA DOKONČIŤ

### 1. EPO API Integration (KRITICKÉ) 🔴

**Problém:** EPO service má len skeleton - reálny parsing chýba.

**Úlohy:**
```python
# app/services/epo_service.py

# TODO 1: Implementovať parsing EPO XML/JSON response
async def _parse_epo_response(self, patent_number: str, raw_data: Dict):
    # Extrahovať:
    # - Legal status (active/expired)
    # - Designated states (DE, FR, etc.)
    # - Expiry date
    # - Lapse events (fees not paid, withdrawn, etc.)
    pass

# TODO 2: Testovať s reálnym EPO API
# - Získaj testovací patent number
# - Verify OAuth2 token flow
# - Handle rate limits (1000 req/week)
```

**Príklad EPO response** (zjednodušené):
```json
{
  "ops:world-patent-data": {
    "exchange-documents": {
      "exchange-document": {
        "bibliographic-data": {
          "publication-reference": {...},
          "application-reference": {...}
        }
      }
    }
  }
}
```

**Resources:**
- EPO OPS API Docs: https://www.epo.org/searching-for-patents/data/web-services/ops.html
- Test endpoint: `GET /rest-services/published-data/publication/epodoc/EP1000000`

---

### 2. USPTO API Integration (VYSOKÁ PRIORITA) 🟡

**Problém:** USPTO service má len skeleton - reálny parsing chýba.

**Úlohy:**
```python
# app/services/uspto_service.py

# TODO 1: Implementovať parsing USPTO response
async def _parse_uspto_response(self, patent_number: str, raw_data: Dict):
    # Extrahovať:
    # - Patent status
    # - Maintenance fee status (critical!)
    # - Expiry date calculation
    pass

# TODO 2: Testovať s USPTO API
# Example: US10000000
```

**USPTO API:**
- Base URL: `https://developer.uspto.gov/ds-api`
- Docs: https://developer.uspto.gov/api-catalog

---

### 3. Testing (VYSOKÁ PRIORITA) 🟡

**Úlohy:**
```bash
# tests/test_epo_service.py
- Test OAuth2 authentication
- Mock EPO responses
- Test error handling (404, 500, rate limits)

# tests/test_uspto_service.py
- Mock USPTO responses
- Test parsing logic

# tests/test_cache_service.py
- Test cache hits/misses
- Test TTL expiration
- Test popularity tracking

# tests/test_rate_limiter.py
- Test tier limits (free, basic, pro)
- Test monthly reset
- Test 429 errors
```

**Run tests:**
```bash
pytest --cov=app tests/
```

---

### 4. RapidAPI Integration (STREDNÁ PRIORITA) 🟢

**Úlohy:**
1. [ ] Create RapidAPI account
2. [ ] Upload API to RapidAPI
3. [ ] Set pricing tiers
4. [ ] Add description & documentation
5. [ ] Test with RapidAPI headers
6. [ ] Publish & market

**RapidAPI Headers to test:**
```bash
curl -H "X-RapidAPI-Proxy-Secret: your_secret" \
     -H "X-RapidAPI-Subscription: pro" \
     -H "X-RapidAPI-Key: user_api_key" \
     "http://localhost:8000/api/v1/status?patent=EP1234567"
```

---

### 5. Production Improvements (NÍZKA PRIORITA) 🔵

#### Redis Cache (Optional)
Nahradiť in-memory rate limiter za Redis:
```python
# requirements.txt
redis==5.0.1
```

```python
# app/utils/rate_limiter.py
import redis
r = redis.Redis(host='localhost', port=6379)
```

#### Async PostgreSQL
Upgrade na async SQLAlchemy:
```python
# requirements.txt
sqlalchemy[asyncio]==2.0.25

# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
```

#### Monitoring
- [ ] Add Sentry for error tracking
- [ ] Add Prometheus metrics
- [ ] Set up UptimeRobot alerts

#### Performance
- [ ] Add database indexes
- [ ] Optimize SQL queries
- [ ] Add caching headers (ETags)
- [ ] Implement batch endpoint

---

## 🎯 Development Roadmap

### Week 1: Core Functionality
- [ ] Implement EPO parsing
- [ ] Implement USPTO parsing
- [ ] Test with real API keys
- [ ] Fix any bugs

### Week 2: Testing & Polish
- [ ] Write comprehensive tests
- [ ] Add more error handling
- [ ] Improve documentation
- [ ] Test locally with Docker

### Week 3: Deployment
- [ ] Deploy to Render.com
- [ ] Run migrations
- [ ] Test in production
- [ ] Monitor logs

### Week 4: RapidAPI & Marketing
- [ ] Integrate with RapidAPI
- [ ] Create API description
- [ ] Set pricing
- [ ] Publish & market

---

## 🐛 Known Issues & Limitations

### Current Limitations:
1. **No batch API** - len single patent lookup (v2 feature)
2. **In-memory rate limiting** - reštartom sa reset (use Redis pre production)
3. **No auto-refresh** - cache sa updatuje len on-demand
4. **EPO/USPTO parsing incomplete** - potrebuje real API testing
5. **No webhook notifications** - v2 feature

### Security Considerations:
- [ ] Add rate limiting per IP (prevent abuse)
- [ ] Add input sanitization (SQL injection protection)
- [ ] Add request signature validation (RapidAPI)
- [ ] Add API key rotation mechanism

---

## 📚 Learning Resources

### EPO OPS API:
- Registration: https://www.epo.org/searching-for-patents/data/web-services/ops.html
- Documentation: https://www.epo.org/searching-for-patents/data/web-services/ops_documentation.html
- Code examples: GitHub has Python EPO clients

### USPTO API:
- API Portal: https://developer.uspto.gov/
- Patent Search API: https://developer.uspto.gov/api-catalog/patent-search-api

### RapidAPI:
- Provider Guide: https://docs.rapidapi.com/docs/provider-quick-start-guide
- Best Practices: https://docs.rapidapi.com/docs/best-practices

---

## 💡 Future Features (v2)

### Batch API
```python
POST /api/v1/batch
{
  "patents": ["EP1234567", "US7654321", "EP9876543"]
}
```

### Webhook Notifications
```python
POST /api/v1/webhooks
{
  "url": "https://your-app.com/webhook",
  "patents": ["EP1234567"],
  "events": ["status_change", "expiry_warning"]
}
```

### Patent Family Info
```python
GET /api/v1/family?patent=EP1234567
# Returns all related patents in family
```

### Historical Data
```python
GET /api/v1/history?patent=EP1234567
# Returns legal status changes over time
```

---

## 🚀 Quick Start for Development

```bash
# 1. Clone & setup
git clone https://github.com/your-username/patent-expiration-api.git
cd patent-expiration-api
./setup.sh

# 2. Add API keys to .env
# EPO_CONSUMER_KEY=...
# EPO_CONSUMER_SECRET=...
# USPTO_API_KEY=...

# 3. Start database
docker-compose up db

# 4. Run migrations
alembic upgrade head

# 5. Start API
uvicorn app.main:app --reload

# 6. Test
curl http://localhost:8000/api/v1/health
```

---

**Priorita úloh:**
1. 🔴 EPO/USPTO parsing (CRITICAL)
2. 🟡 Testing (HIGH)
3. 🟡 Deployment (HIGH)
4. 🟢 RapidAPI (MEDIUM)
5. 🔵 Redis/optimization (LOW)

**Good luck! 🚀**
