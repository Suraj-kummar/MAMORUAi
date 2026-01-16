# 📖 Step-by-Step Guide to Run MamoruAI

Follow these steps carefully to get MamoruAI running on your machine.

---

## ✅ Step 1: Check Prerequisites

### 1.1 Install Docker Desktop

1. Go to https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for Windows
3. Install and launch Docker Desktop
4. Wait for Docker to start (whale icon in system tray should be steady)
5. Verify installation:
   ```bash
   docker --version
   docker compose version
   ```

### 1.2 Get API Keys

**Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with something like `AIza...`)

**Etherscan API Key:**
1. Go to https://etherscan.io/apis
2. Sign up for a free account
3. Go to "API-KEYs" section
4. Create a new API key
5. Copy the key

---

## ✅ Step 2: Setup Environment Variables

### 2.1 Create .env File

1. Open the project folder: `C:\Users\suraj\OneDrive\Desktop\MamoruAI`
2. Check if `.env` file exists in the root folder
3. If it doesn't exist, create a new file named `.env` (no extension)
4. If `.env.example` exists, you can copy it and rename to `.env`

### 2.2 Add Your API Keys

Open `.env` file in a text editor and add:

```env
GEMINI_API_KEY=your_actual_gemini_key_here
ETHERSCAN_API_KEY=your_actual_etherscan_key_here
INNGEST_EVENT_KEY=
INNGEST_SIGNING_KEY=
```

**Important:** 
- Replace `your_actual_gemini_key_here` with your real Gemini API key
- Replace `your_actual_etherscan_key_here` with your real Etherscan API key
- Leave Inngest keys empty for now (optional)

**Example:**
```env
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ETHERSCAN_API_KEY=YourEtherscanAPIKey123456
INNGEST_EVENT_KEY=
INNGEST_SIGNING_KEY=
```

---

## ✅ Step 3: Start Docker Services

### 3.1 Open Terminal/Command Prompt

1. Open Command Prompt or PowerShell
2. Navigate to project folder:
   ```bash
   cd C:\Users\suraj\OneDrive\Desktop\MamoruAI
   ```

### 3.2 Start All Services

**Option A: Using Docker Compose (Recommended)**

Try this first:
```bash
docker compose up --build
```

If that doesn't work, try:
```bash
docker-compose up --build
```

**What this does:**
- Builds Docker images for frontend and engine
- Starts PostgreSQL database
- Starts Redis queue
- Starts Python analysis engine
- Starts Next.js frontend

**Expected output:**
You'll see logs from all services. Wait until you see:
- `frontend-1  | ready - started server on 0.0.0.0:3000`
- `engine-1    | Application startup complete`

**Note:** First time will take 5-10 minutes to download images and build.

### 3.3 Run in Background (Optional)

If you want to run in background:
```bash
docker compose up --build -d
```

Then view logs with:
```bash
docker compose logs -f
```

---

## ✅ Step 4: Setup Database

### 4.1 Open New Terminal

Keep the Docker terminal running, open a **NEW** terminal window.

### 4.2 Navigate to Frontend Folder

```bash
cd C:\Users\suraj\OneDrive\Desktop\MamoruAI\frontend
```

### 4.3 Run Database Migrations

```bash
npx prisma migrate dev --name init
```

**What this does:**
- Creates database tables
- Sets up schema for contracts, audits, vulnerabilities

**Expected output:**
```
✔ Generated Prisma Client
The following migration(s) have been created and applied...
```

### 4.4 Generate Prisma Client

```bash
npx prisma generate
```

**Expected output:**
```
✔ Generated Prisma Client
```

---

## ✅ Step 5: Verify Everything is Running

### 5.1 Check Docker Containers

In your Docker terminal or new terminal:
```bash
docker compose ps
```

You should see 4 services running:
- `db` (PostgreSQL)
- `queue` (Redis)
- `engine` (Python API)
- `frontend` (Next.js)

### 5.2 Test Health Endpoint

Open browser and go to:
```
http://localhost:8000/health
```

You should see JSON response with health status.

### 5.3 Check Frontend

Open browser and go to:
```
http://localhost:3000
```

You should see the MamoruAI landing page.

---

## ✅ Step 6: Run Your First Audit

### 6.1 Go to Dashboard

1. Open browser: http://localhost:3000/dashboard
2. You should see the "COMMAND CENTER" dashboard

### 6.2 Enter Contract Address

1. In the input field, enter a verified contract address
2. Example addresses to try:
   - `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (USDC)
   - `0xdAC17F958D2ee523a2206206994597C13D831ec7` (USDT)
   - `0x6B175474E89094C44Da98b954EedeAC495271d0F` (DAI)

### 6.3 Trigger Audit

1. Click "Trigger Security Audit" button
2. Wait 30-60 seconds
3. You'll be redirected to the audit results page
4. Watch the analysis progress:
   - Fetching source code
   - Running Slither analysis
   - AI contextualization
   - Results display

### 6.4 View Results

You'll see:
- Security score (0-100)
- List of vulnerabilities
- AI-generated explanations
- Source code with highlighted issues

---

## 🛠️ Troubleshooting

### Problem: Docker not starting

**Solution:**
1. Make sure Docker Desktop is running
2. Check if virtualization is enabled in BIOS
3. Restart Docker Desktop

### Problem: Port already in use

**Solution:**
```bash
# Check what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Stop the process or change ports in docker-compose.yml
```

### Problem: Database connection error

**Solution:**
1. Wait 30 seconds for PostgreSQL to fully start
2. Check if `db` container is running: `docker compose ps`
3. Restart database: `docker compose restart db`

### Problem: API key errors

**Solution:**
1. Double-check `.env` file has correct keys
2. Make sure no extra spaces or quotes
3. Restart containers: `docker compose restart`

### Problem: Prisma migration fails

**Solution:**
```bash
# Reset database
cd frontend
npx prisma migrate reset
npx prisma migrate dev --name init
npx prisma generate
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f engine
docker compose logs -f frontend
docker compose logs -f db
```

---

## 🛑 Stop the Project

When you're done:

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clears database)
docker compose down -v
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard

---

## ✅ Quick Checklist

- [ ] Docker Desktop installed and running
- [ ] `.env` file created with API keys
- [ ] `docker compose up --build` completed successfully
- [ ] Database migrations run (`npx prisma migrate dev`)
- [ ] Health check works (http://localhost:8000/health)
- [ ] Frontend loads (http://localhost:3000)
- [ ] First audit completed successfully

---

**Need Help?** Check the logs or see [QUICKSTART.md](QUICKSTART.md) for more details.
