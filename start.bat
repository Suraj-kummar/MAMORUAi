@echo off
REM MamoruAI Startup Script for Windows

echo 🛡️  Starting MamoruAI...

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from .env.example...
    if exist .env.example (
        copy .env.example .env
        echo 📝 Please edit .env and add your API keys:
        echo    - GEMINI_API_KEY
        echo    - ETHERSCAN_API_KEY
        echo.
        pause
    ) else (
        echo ❌ .env.example not found. Please create .env manually.
        exit /b 1
    )
)

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo 🐳 Starting Docker containers...
docker-compose up --build -d

echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Setup database
echo 🗄️  Setting up database...
cd frontend
call npx prisma migrate deploy 2>nul || call npx prisma migrate dev --name init
call npx prisma generate
cd ..

echo.
echo ✅ MamoruAI is starting up!
echo.
echo 📍 Services:
echo    - Frontend: http://localhost:3000
echo    - Engine API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
echo 📊 View logs: docker-compose logs -f
echo 🛑 Stop: docker-compose down
echo.

pause
