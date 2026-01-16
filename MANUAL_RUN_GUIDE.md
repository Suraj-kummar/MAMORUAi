# 🛠️ MamoruAI Manual Run Guide

Follow these steps to run the project locally on Windows.

## 1. Prerequisites
- **Node.js v20+** (Required for Prisma/Next.js compatibility)
- **Python 3.11+**
- **Docker Desktop** (For Database & Redis)

## 2. Environment Setup
Check that your root `.env` file exists and has your API keys:
- `GEMINI_API_KEY`
- `ETHERSCAN_API_KEY`

## 3. Infrastructure (Docker)
Instead of running everything in Docker, we will only run the database and queue:
```bash
docker-compose up -d db queue
```

## 4. Backend (Engine) Setup
Open a new terminal:
```bash
cd engine
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*The engine will be available at http://localhost:8000*

## 5. Frontend Setup
Open another terminal:
```bash
cd frontend
# 1. Install dependencies (using legacy-peer-deps due to React 19/ConnectKit conflict)
npm install --legacy-peer-deps

# 2. Setup Database
npx prisma generate
npx prisma migrate dev --name init

# 3. Start development server
npm run dev
```
*The frontend will be available at http://localhost:3000*

---

### ✅ Fixes Already Applied
I have already fixed several issues in the codebase for you:
1.  **Next.js 15+ Params**: Updated API routes (`audit` and `contract`) to handle the new asynchronous `params` requirements.
2.  **Docker Optimization**: Added `.dockerignore` to keep your containers lean.
3.  **Node.js Version**: Updated Dockerfile to use Node 20.
4.  **Peer Dependencies**: Identified the React 19 / ConnectKit conflict.
