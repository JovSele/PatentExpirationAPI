# 📊 Patent Expiration API - Project Summary

## 🎯 Koncept
B2B Micro-Service API pre overenie statusu patentov (aktívny/expirovaný) s predajom cez RapidAPI.

## ✨ Core Value
**"Je tento patent aktívny a kde?"** - jednoduchá odpoveď na 3 otázky:
1. Status: active/expired
2. Expiry date
3. Jurisdikcie (EP, US, DE, FR...)

---

## 🏗️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL (cache + analytics)
- **APIs:** EPO OPS + USPTO
- **Hosting:** Render.com (free tier)
- **Marketplace:** RapidAPI

### Architektúra
```
User → RapidAPI → Your API → Cache (PostgreSQL) → EPO/USPTO APIs
```

---

## 📁 Project Structure

```
patent-expiration-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── models.py            # DB models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # DB connection
│   ├── api/v1/
│   │   ├── endpoints.py     # API routes
│   │   └── dependencies.py  # Shared dependencies
│   ├── services/
│   │   ├── epo_service.py   # EPO integration
│   │   ├── uspto_service.py # USPTO integration
│   │   └── cache_service.py # Cache logic
│   └── utils/
│       ├── normalizer.py    # Data normalization
│       └── rate_limiter.py  # Rate limiting
├── tests/                   # Test suite
├── alembic/                 # DB migrations
├── Dockerfile               # Container
├── docker-compose.yml       # Local dev
├── render.yaml              # Render config
├── requirements.txt         # Dependencies
├── PLAN.md                  # Development plan
├── DEPLOYMENT.md            # Deploy guide
├── NEXT_STEPS.md            # TODO list
└── README.md                # Setup guide
```

---

## 🚀 Quick Start

### Local Development
```bash
# 1. Setup
./setup.sh

# 2. Add API keys to .env
# EPO_CONSUMER_KEY=...
# EPO_CONSUMER_SECRET=...

# 3. Start database
docker-compose up db

# 4. Migrate
alembic upgrade head

# 5. Run
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

### Deploy to Render.com
```bash
# 1. Push to GitHub
git push origin main

# 2. Connect Render.com
# 3. Add environment variables
# 4. Deploy!
```

---

## 📊 API Endpoints

### Main Endpoints
```bash
GET /api/v1/status?patent=EP1234567
GET /api/v1/health
GET /disclaimer
```

### Response Format
```json
{
  "patent": "EP1234567",
  "status": "expired",
  "expiry_date": "2021-11-04",
  "jurisdictions": ["EP", "DE", "FR"],
  "lapse_reason": "fee not paid",
  "source": "EPO",
  "last_update": "2025-11-11T10:30:00Z",
  "disclaimer": "For informational purposes only..."
}
```

---

## 💰 Pricing Model (RapidAPI)

| Tier       | Requests/Month | Price      |
|------------|----------------|------------|
| Free       | 20             | €0         |
| Basic      | 1,000          | €19/month  |
| Pro        | 10,000         | €99/month  |
| Enterprise | Custom         | Contact    |

---

## ✅ MVP Status

### COMPLETED (75%)
- [x] Project structure
- [x] FastAPI app with CORS & middleware
- [x] PostgreSQL models (cache + logging)
- [x] Rate limiting (RapidAPI tiers)
- [x] EPO service skeleton (OAuth2)
- [x] USPTO service skeleton
- [x] Cache system (30-day TTL)
- [x] Legal disclaimers
- [x] Docker setup
- [x] Render deployment config
- [x] Documentation (README, DEPLOYMENT, etc.)
- [x] Basic tests

### TODO (25%)
- [ ] EPO API parsing (CRITICAL)
- [ ] USPTO API parsing (CRITICAL)
- [ ] Comprehensive testing
- [ ] RapidAPI integration
- [ ] Production deployment
- [ ] Monitoring & analytics

---

## 🎯 Next Steps

### Week 1: Core Functionality
1. Získať EPO API keys (register na epo.org)
2. Získať USPTO API key (developer.uspto.gov)
3. Implementovať EPO response parsing
4. Implementovať USPTO response parsing
5. Testovať s reálnymi patentmi

### Week 2: Testing
1. Mock API responses
2. Test cache behavior
3. Test rate limiting
4. Fix bugs

### Week 3: Deployment
1. Deploy to Render.com
2. Setup PostgreSQL
3. Run migrations
4. Monitor logs

### Week 4: Launch
1. Integrate RapidAPI
2. Set pricing
3. Write marketing copy
4. Publish!

---

## 📚 Key Documents

- **PLAN.md** - Development checklist (track progress)
- **README.md** - Setup instructions
- **DEPLOYMENT.md** - Deploy guide (Render/Railway/Fly.io)
- **NEXT_STEPS.md** - Detailed TODO list
- **COMMANDS.md** - Useful commands reference

---

## 🐛 Known Limitations (MVP)

1. **EPO/USPTO parsing incomplete** - needs real API testing
2. **No batch API** - only single patent lookup (v2)
3. **In-memory rate limiting** - use Redis for production
4. **No auto-refresh** - cache updates on-demand only
5. **Basic error handling** - needs more edge cases

---

## 🛡️ Legal Protection

✅ **Strong disclaimers:**
- "For informational purposes only"
- "Not legal advice"
- "No warranty"
- Limiting liability

✅ **User responsibility:**
- Always verify with official sources
- Consult patent attorney for legal matters

---

## 📈 Success Metrics

### Technical
- Response time: < 2s (cache: < 200ms)
- Uptime: > 99%
- Error rate: < 1%

### Business
- 10 users in first 30 days
- 100+ API calls/month
- 5% conversion (free → paid)

---

## 🎉 What Makes This Great

1. **Simple Value Prop** - answers one question well
2. **Low Liability** - strong disclaimers
3. **Minimal Maintenance** - cache reduces API calls
4. **Scalable** - start free, grow to paid
5. **Clear Pricing** - credit-based model
6. **Good Documentation** - easy to use

---

## 💡 Future Features (v2)

- [ ] Batch API (multiple patents at once)
- [ ] Webhook notifications (status changes)
- [ ] Patent family info
- [ ] Historical data (legal events timeline)
- [ ] More jurisdictions (JP, CN, KR...)

---

**Status:** 🚧 MVP Ready for Testing  
**Estimate to Launch:** 2-3 týždne  
**Initial Investment:** €0 (free tier everywhere)

**Next Action:** Get EPO & USPTO API keys → Test parsing → Deploy 🚀
