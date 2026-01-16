# 🚀 How to Run MamoruAI

## Quick Start (3 Steps)

### 1. Setup Environment

Create a `.env` file in the project root with your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
ETHERSCAN_API_KEY=your_etherscan_api_key
```

**Get API Keys:**
- Gemini: https://makersuite.google.com/app/apikey
- Etherscan: https://etherscan.io/apis (free tier works)

### 2. Start with Docker

**If you have Docker Compose v2 (newer):**
```bash
docker compose up --build
```

**If you have Docker Compose v1 (older):**
```bash
docker-compose up --build
```

### 3. Setup Database

In a new terminal:
```bash
cd frontend
npx prisma migrate dev --name init
npx prisma generate
```

## Access the Application

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Run Your First Audit

1. Go to http://localhost:3000/dashboard
2. Enter a contract address (e.g., `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`)
3. Click "Trigger Security Audit"
4. Wait 30-60 seconds for results

## Troubleshooting

**Check if services are running:**
```bash
docker ps
```

**View logs:**
```bash
docker compose logs -f
# or
docker-compose logs -f
```

**Stop services:**
```bash
docker compose down
# or
docker-compose down
```

**Restart a service:**
```bash
docker compose restart engine
```

## Manual Setup (Without Docker)

See [QUICKSTART.md](QUICKSTART.md) for manual setup instructions.
