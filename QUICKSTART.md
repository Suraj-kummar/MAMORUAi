# 🚀 Quick Start Guide

## Prerequisites

- **Docker Desktop** installed and running
- **API Keys**:
  - Gemini API Key: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Etherscan API Key: Get from [Etherscan](https://etherscan.io/apis) (free tier works)

## Step 1: Setup Environment Variables

1. Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env
```

2. Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_actual_gemini_key_here
ETHERSCAN_API_KEY=your_actual_etherscan_key_here
```

> **Note**: Inngest keys are optional for local development. Leave them empty if you don't have them.

## Step 2: Start the Project

### Option A: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Option B: Using Startup Script

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

## Step 3: Setup Database

After containers are running, setup the database:

```bash
cd frontend
npx prisma migrate dev --name init
npx prisma generate
cd ..
```

## Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Engine API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 5: Run Your First Audit

1. Open http://localhost:3000/dashboard
2. Enter a verified contract address (e.g., `0x...`)
3. Click "Trigger Security Audit"
4. Wait for analysis to complete (usually 30-60 seconds)
5. View results on the audit page

## Troubleshooting

### Check Service Status

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f engine
docker-compose logs -f frontend
docker-compose logs -f db
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart engine
```

### Stop Services

```bash
docker-compose down

# Remove volumes (clears database)
docker-compose down -v
```

### Common Issues

1. **Port already in use**: Stop other services using ports 3000, 8000, 5432, or 6379
2. **API key errors**: Make sure `.env` file has correct API keys
3. **Database connection errors**: Wait a few seconds for PostgreSQL to start
4. **Slither not found**: The Dockerfile should install it automatically

## Development Mode

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

### Run Engine Locally

```bash
cd engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
