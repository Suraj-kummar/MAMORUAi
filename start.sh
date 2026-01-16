#!/bin/bash

# MamoruAI Startup Script

echo "🛡️  Starting MamoruAI..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Please edit .env and add your API keys:"
        echo "   - GEMINI_API_KEY"
        echo "   - ETHERSCAN_API_KEY"
        echo ""
        read -p "Press Enter after adding your API keys..."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Starting Docker containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if database is ready
echo "🗄️  Setting up database..."
cd frontend
npx prisma migrate deploy || npx prisma migrate dev --name init
npx prisma generate
cd ..

echo ""
echo "✅ MamoruAI is starting up!"
echo ""
echo "📍 Services:"
echo "   - Frontend: http://localhost:3000"
echo "   - Engine API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down"
echo ""
