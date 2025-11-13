#!/bin/bash
# Setup script for Patent Expiration API

set -e  # Exit on error

echo "🚀 Setting up Patent Expiration API..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
fi

# Initialize database
echo "🗄️  Initializing database..."
echo "⚠️  Make sure PostgreSQL is running and DATABASE_URL is set in .env"
echo "Run: alembic upgrade head"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys (EPO_CONSUMER_KEY, EPO_CONSUMER_SECRET)"
echo "2. Start PostgreSQL (or use docker-compose up db)"
echo "3. Run migrations: alembic upgrade head"
echo "4. Start development server: uvicorn app.main:app --reload"
echo ""
echo "📖 See README.md for more details"
