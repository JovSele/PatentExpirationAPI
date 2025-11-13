# Quick Reference - Useful Commands

## 🚀 Setup & Installation

```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## 🐳 Docker Commands

```bash
# Start everything (database + API)
docker-compose up --build

# Start only database
docker-compose up db

# Stop all services
docker-compose down

# View logs
docker-compose logs -f api

# Rebuild after code changes
docker-compose up --build api
```

## 🗄️ Database Commands

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_endpoints.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

## 🏃 Development Server

```bash
# Start with auto-reload
uvicorn app.main:app --reload

# Start on specific port
uvicorn app.main:app --reload --port 8080

# Start with custom host
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Database Inspection

```bash
# Connect to PostgreSQL (local)
psql postgresql://patent_user:patent_password@localhost:5432/patent_api

# Useful SQL queries:
SELECT * FROM patent_cache LIMIT 10;
SELECT * FROM request_log ORDER BY created_at DESC LIMIT 10;
SELECT COUNT(*) FROM patent_cache;

# Most requested patents
SELECT patent_number, fetch_count 
FROM patent_cache 
ORDER BY fetch_count DESC 
LIMIT 10;

# Request stats by tier
SELECT user_tier, COUNT(*) as count 
FROM request_log 
GROUP BY user_tier;
```

## 🔧 Maintenance

```bash
# Check code style
black --check app/
flake8 app/

# Format code
black app/

# Type checking
mypy app/

# Clear cache (SQL)
DELETE FROM patent_cache WHERE last_fetched < NOW() - INTERVAL '30 days';
```

## 🌐 API Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Get patent status
curl "http://localhost:8000/api/v1/status?patent=EP1234567"

# With RapidAPI headers
curl -H "X-RapidAPI-Proxy-Secret: your_secret" \
     -H "X-RapidAPI-Subscription: pro" \
     "http://localhost:8000/api/v1/status?patent=EP1234567"

# Check rate limits (look for X-RateLimit-* headers)
curl -i "http://localhost:8000/api/v1/status?patent=EP1234567"
```

## 📦 Deployment (Render.com)

```bash
# 1. Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Connect Render.com to GitHub repo
# 3. Set environment variables in Render dashboard:
#    - EPO_CONSUMER_KEY
#    - EPO_CONSUMER_SECRET
#    - USPTO_API_KEY
#    - DATABASE_URL (auto-set by Render)
#    - RAPIDAPI_PROXY_SECRET

# 4. Deploy automatically triggers on push
```

## 🔍 Logs & Monitoring

```bash
# View Docker logs
docker-compose logs -f api

# View specific service logs
docker-compose logs -f db

# Tail local logs
tail -f logs/app.log

# Filter error logs
grep "ERROR" logs/app.log
```

## 🧹 Cleanup

```bash
# Remove all Docker containers and volumes
docker-compose down -v

# Remove virtual environment
rm -rf venv/

# Remove cache files
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove database (careful!)
docker-compose down -v
```

## 📚 Documentation

```bash
# View API docs (after starting server)
open http://localhost:8000/docs

# View ReDoc
open http://localhost:8000/redoc

# View root info
curl http://localhost:8000/
```

## 🐛 Debugging

```bash
# Start in debug mode
DEBUG=true uvicorn app.main:app --reload

# Check environment variables
python -c "from app.config import settings; print(settings.dict())"

# Test database connection
python -c "from app.database import engine; engine.connect()"

# Interactive Python shell with app context
python
>>> from app.main import app
>>> from app.database import SessionLocal
>>> db = SessionLocal()
```
