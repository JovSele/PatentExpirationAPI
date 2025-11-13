# 🚀 Deployment Guide - Patent Expiration API

Complete guide pre nasadenie API na **Render.com**, **Railway.app**, alebo **Fly.io**.

---

## 🎯 Pre-Deployment Checklist

- [ ] EPO OPS API klúče (Consumer Key + Consumer Secret)
- [ ] USPTO API klúč (voliteľné)
- [ ] GitHub repository
- [ ] RapidAPI account (pre marketplace)

---

## 📦 Option 1: Render.com (ODPORÚČANÉ)

**Prečo Render:**
- ✅ 1GB PostgreSQL zadarmo
- ✅ Jednoduchý setup
- ✅ Automatický deployment z GitHub
- ✅ HTTPS zadarmo

### Krok po kroku:

#### 1. Push to GitHub
```bash
cd patent-expiration-api
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/patent-expiration-api.git
git push -u origin main
```

#### 2. Create Render Account
- Choď na https://render.com
- Sign up with GitHub

#### 3. Create PostgreSQL Database
1. Dashboard → New → PostgreSQL
2. Name: `patent-api-db`
3. Plan: **Free** (1GB storage)
4. Create Database
5. **Skopíruj Internal Database URL** (potrebuješ ju neskôr)

#### 4. Create Web Service
1. Dashboard → New → Web Service
2. Connect GitHub repository
3. Settings:
   - **Name:** `patent-expiration-api`
   - **Region:** Frankfurt (EU) alebo najbližší
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

#### 5. Add Environment Variables
V Render Dashboard → Web Service → Environment:

```
DATABASE_URL = [skopíruj z PostgreSQL Internal URL]
EPO_CONSUMER_KEY = [tvoj EPO klúč]
EPO_CONSUMER_SECRET = [tvoj EPO secret]
USPTO_API_KEY = [tvoj USPTO klúč]
SECRET_KEY = [vygeneruj random: openssl rand -hex 32]
RAPIDAPI_PROXY_SECRET = [nastaviť neskôr pre RapidAPI]
ENVIRONMENT = production
DEBUG = false
```

#### 6. Deploy!
- Klikni "Create Web Service"
- Počkaj 5-10 minút na build
- API bude dostupné na: `https://patent-expiration-api.onrender.com`

#### 7. Run Database Migrations
V Render Dashboard → Shell:
```bash
alembic upgrade head
```

#### 8. Test API
```bash
curl https://patent-expiration-api.onrender.com/api/v1/health
```

---

## 📦 Option 2: Railway.app

**Prečo Railway:**
- ✅ 512MB PostgreSQL zadarmo
- ✅ $5 credit každý mesiac
- ✅ Rýchlejší cold start

### Krok po kroku:

#### 1. Create Railway Account
- https://railway.app
- Sign up with GitHub

#### 2. Create New Project
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
cd patent-expiration-api
railway init
```

#### 3. Add PostgreSQL
```bash
railway add postgresql
```

#### 4. Deploy
```bash
# Set environment variables
railway variables set EPO_CONSUMER_KEY=your_key
railway variables set EPO_CONSUMER_SECRET=your_secret
railway variables set USPTO_API_KEY=your_key

# Deploy
railway up
```

#### 5. Get URL
```bash
railway domain
```

---

## 📦 Option 3: Fly.io

**Prečo Fly:**
- ✅ Edge locations (nízka latencia)
- ✅ Free tier: 3 shared-cpu VMs
- ✅ Global deployment

### Krok po kroku:

#### 1. Install Fly CLI
```bash
# Mac
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login
```

#### 2. Create App
```bash
cd patent-expiration-api
flyctl launch
# Answer prompts:
# - App name: patent-expiration-api
# - Region: fra (Frankfurt)
# - PostgreSQL: Yes
# - Deploy: No (need to set secrets first)
```

#### 3. Set Secrets
```bash
flyctl secrets set EPO_CONSUMER_KEY=your_key
flyctl secrets set EPO_CONSUMER_SECRET=your_secret
flyctl secrets set USPTO_API_KEY=your_key
flyctl secrets set SECRET_KEY=$(openssl rand -hex 32)
```

#### 4. Deploy
```bash
flyctl deploy
```

#### 5. Open App
```bash
flyctl open
```

---

## 🔧 Post-Deployment Setup

### 1. Run Database Migrations
Každý hosting má CLI pre shell access:

**Render:**
```bash
# Dashboard → Shell
alembic upgrade head
```

**Railway:**
```bash
railway run alembic upgrade head
```

**Fly.io:**
```bash
flyctl ssh console
alembic upgrade head
```

### 2. Test All Endpoints
```bash
BASE_URL=https://your-api.onrender.com

# Health check
curl $BASE_URL/api/v1/health

# Patent lookup (will fail without valid patent, but tests endpoint)
curl "$BASE_URL/api/v1/status?patent=EP1234567"

# Legal disclaimer
curl $BASE_URL/disclaimer
```

### 3. Monitor Logs
**Render:** Dashboard → Logs
**Railway:** `railway logs`
**Fly.io:** `flyctl logs`

---

## 🏪 RapidAPI Integration

### 1. Create RapidAPI Account
- https://rapidapi.com/provider
- Sign up as Provider

### 2. Add New API
1. Dashboard → My APIs → Add New API
2. **Name:** Patent Expiration API
3. **Category:** Data
4. **Base URL:** `https://your-api.onrender.com`

### 3. Configure Endpoints
Add endpoint:
- **Path:** `/api/v1/status`
- **Method:** GET
- **Parameters:** 
  - `patent` (query, required) - Patent number

### 4. Set Pricing
1. Dashboard → Pricing
2. Create plans:
   - **Free:** 20 requests/month - €0
   - **Basic:** 1,000 requests/month - €19
   - **Pro:** 10,000 requests/month - €99

### 5. Add Documentation
- Description
- Use cases
- Example requests
- Legal disclaimer

### 6. Publish
- Test all endpoints
- Submit for review
- Go live! 🎉

---

## 📊 Monitoring & Maintenance

### Health Checks
Nastav monitoring (napr. UptimeRobot, Better Uptime):
- Endpoint: `https://your-api.onrender.com/api/v1/health`
- Interval: 5 minutes
- Alert: Email ak down

### Database Backups
**Render:** Automatické (paid plans)
**Railway:** Automatické
**Fly.io:** `flyctl postgres backup`

### Scaling
Ak free tier nestačí:
- **Render:** Upgrade to Starter ($7/month)
- **Railway:** $5 credit/month (usually enough)
- **Fly.io:** Pay-as-you-go

---

## 🐛 Troubleshooting

### "Database connection failed"
- Skontroluj DATABASE_URL environment variable
- Verify PostgreSQL je running
- Check network connectivity

### "EPO API authentication failed"
- Verify EPO_CONSUMER_KEY a EPO_CONSUMER_SECRET
- Check OAuth token expiration
- Test credentials lokálne

### "Rate limit exceeded"
- Implementuj Redis pre lepší rate limiting (pre production)
- Alebo upgrade na paid tier s väčším DB

### "Slow response times"
- Check cache hit rate: `SELECT COUNT(*) FROM patent_cache;`
- Optimize database queries
- Consider adding Redis cache

---

## 📚 Resources

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Fly.io Docs:** https://fly.io/docs
- **RapidAPI Docs:** https://docs.rapidapi.com/docs/provider-quick-start-guide
- **EPO OPS Docs:** https://www.epo.org/searching-for-patents/data/web-services/ops.html

---

**Úspešný deployment! 🎉**

Ďalšie kroky:
1. Test all endpoints thoroughly
2. Integrate with RapidAPI
3. Market your API
4. Monitor usage and iterate
