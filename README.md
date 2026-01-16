# 🛡️ MamoruAI (守るAI) - Zero-G Security for Web3

> **"In Web3, traditional security 'gravity' doesn't exist. MamoruAI is the life-support system for your logic."**

MamoruAI is an AI-driven smart contract security scanner designed for the **Zero-Gravity Environment** of decentralized finance. While traditional scanners assume ground-level protection with firewalls and centralized oversight, MamoruAI treats every line of code as if it's floating in the vacuum of space—where a single vulnerability can eject your entire capital into the void.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 🌌 The Antigravity Principle: Zero-G Security

Most scanners assume a **"Ground-Level"** environment where firewalls and centralized oversight act as gravity. MamoruAI is built for the **Zero-G Environment** of decentralized finance. We treat every line of code as if it's floating in a vacuum—where there is **no friction** to stop a malicious actor once a leak begins.

### 🛰️ How MamoruAI Defies the "Gravity" of Human Error:

#### 1. **Atmospheric Pressure Testing (Fuzzing)**
We don't just check if the code works; we **"depressurize"** the contract. By injecting thousands of extreme, non-linear inputs, we simulate the "Antigravity" of a chaotic mainnet launch.

- **Traditional Approach**: "Does this function return the expected value?"
- **MamoruAI Approach**: "What happens when we call this function with max uint256, zero addresses, and reentrancy patterns simultaneously?"

#### 2. **The Inertia Engine (AI Reasoning)**
In Zero-G, once an exploit starts, it has **infinite inertia**—it cannot be stopped. MamoruAI uses LLM-orchestrated reasoning (Gemini 1.5 Pro) to predict the momentum of an exploit **before** it is even deployed.

- **Static Analysis**: Slither detects the vulnerability pattern
- **AI Contextualization**: Gemini explains the exploit chain in human language
- **Preventive Patching**: AI-generated Solidity refactoring suggestions

#### 3. **Vacuum-Seal Patching**
Our AI doesn't just suggest a fix; it generates a **"hermetic seal"**—refactored Solidity code that is structurally sound enough to survive the harsh vacuum of permissionless execution.

Example:
```solidity
// ❌ BEFORE: Vulnerable to Reentrancy (No Gravity)
function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount);
    msg.sender.call{value: amount}(""); // EXPLOIT VECTOR
    balances[msg.sender] -= amount;
}

// ✅ AFTER: Vacuum-Sealed (Checks-Effects-Interactions)
function withdraw(uint amount) public nonReentrant {
    require(balances[msg.sender] >= amount, "Insufficient balance");
    balances[msg.sender] -= amount; // STATE UPDATE FIRST
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

---

## 🚀 Architecture Overview

MamoruAI follows a **decoupled microservices architecture** with three core components:

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Next.js UI    │◄────►│  Inngest Queue   │◄────►│ Python Engine   │
│   (Frontend)    │      │  (Orchestration) │      │ (Slither + AI)  │
└─────────────────┘      └──────────────────┘      └─────────────────┘
         │                        │                          │
         └────────────────────────┴──────────────────────────┘
                                  │
                         ┌────────▼────────┐
                         │   PostgreSQL    │
                         │   (Persistence) │
                         └─────────────────┘
```

### Component Breakdown:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Next.js 15, TypeScript, TailwindCSS | Modern Web3 UI with wallet connectivity |
| **Analysis Engine** | Python, FastAPI, Slither | Static analysis + AI-driven contextual explanations |
| **Orchestration** | Inngest | Background job processing, retry logic |
| **Database** | PostgreSQL + Prisma | Audit results persistence |
| **Localization** | next-intl | Bilingual support (EN/JA) |

For detailed architecture diagrams and flow charts, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 📊 The "Senior" Project Impact

| Feature | Traditional Scanner (Earth) | MamoruAI (Zero-G) |
|---------|----------------------------|-------------------|
| **Logic Scoping** | Static & Rigid | Dynamic & Multi-Dimensional |
| **Error Feedback** | "Line 42: Overflow" | "Line 42: AI-Detected Logic Leak. [Fix Here]" |
| **Language Support** | English Only | Bilingual (EN/JA) Global Support |
| **Speed** | Slow/Manual | 60s Automated "Deep-Space" Scan |
| **Exploit Prediction** | Pattern Matching | LLM-Powered Contextual Reasoning |
| **Patch Generation** | Manual Developer Work | AI-Generated Solidity Refactoring |

---
p
## 🛠️ Enhanced Repo Architecture (The Senior Developer Setup)

### 🧬 Observability & Telemetry

Don't just run a script; **monitor the system**.

- **Structured Logging**: Every scan generates a JSON-based trace log, compatible with ELK Stack or Datadog
- **State Machines**: The audit process is governed by a strict finite state machine (FSM), ensuring no scan is left in a "zombie" state during engine failures

```typescript
enum AuditStatus {
  PENDING      → "Scan queued, waiting for worker"
  IN_PROGRESS  → "Slither running, AI reasoning"
  COMPLETED    → "Results stored, ready for review"
  FAILED       → "Engine error, retry logic triggered"
}
```

### 🛡️ Anti-Fragile Infrastructure

- **Dockerized Isolation**: The Python Analysis Engine runs in a hardened, scratch-based Docker container. This prevents **"Audit Contamination"** where one contract's logic could potentially affect the engine's next scan.

- **Redundant LLM Fallbacks**: If the primary AI (Gemini) hits a rate limit, the system automatically fails over to GPT-4o or a local Llama 3 instance to ensure the security "life support" never goes offline.

### 🇯🇵 Global Localization (International Standard)

Because MamoruAI targets the **global Web3 market**, the system is architected with i18n at the core:

- **Bilingual Reports**: Audit summaries are generated in both English and Japanese (守るAIレポート), allowing seamless collaboration between international developer teams and Japanese security firms.
- **Cultural Context**: Japanese Web3 community represents 30%+ of global DeFi TVL—MamoruAI respects this by providing native language support.

---

## 🏗️ Project Structure

```
MamoruAI/
├── frontend/                # Next.js 15 Web UI
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   ├── components/     # Reusable UI components
│   │   ├── lib/            # Prisma client, utilities
│   │   └── messages/       # i18n translations (en.json, ja.json)
│   ├── prisma/
│   │   └── schema.prisma   # Database schema
│   └── package.json
│
├── engine/                  # Python Analysis Engine
│   ├── main.py             # FastAPI server
│   ├── ai_service.py       # Gemini 1.5 Pro integration
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
│
├── docs/
│   └── ARCHITECTURE.md     # Detailed system design
│
└── docker-compose.yml      # Multi-container orchestration
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** installed and running ([Download](https://www.docker.com/products/docker-desktop))
- **API Keys** (see below)

### 1. Environment Setup

```bash
# Create .env file in project root
# Copy .env.example to .env and add your API keys

# Required API Keys:
GEMINI_API_KEY=your_gemini_api_key_here        # Get from: https://makersuite.google.com/app/apikey
ETHERSCAN_API_KEY=your_etherscan_api_key_here  # Get from: https://etherscan.io/apis (free tier works)

# Optional (for Inngest):
INNGEST_EVENT_KEY=
INNGEST_SIGNING_KEY=
```

### 2. Launch the Stack

**Option A: Using Docker Compose (Recommended)**

```bash
# Start all services
docker compose up --build

# Or if you have older Docker Compose:
docker-compose up --build

# Run in background:
docker compose up --build -d
```

**Option B: Using Startup Script**

- **Windows**: Run `start.bat`
- **Linux/Mac**: Run `./start.sh` (make executable first: `chmod +x start.sh`)

### 3. Setup Database

After containers start, run database migrations:

```bash
cd frontend
npx prisma migrate dev --name init
npx prisma generate
cd ..
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Engine API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Run Your First Scan

1. Navigate to `http://localhost:3000/dashboard`
2. Enter a verified contract address (e.g., `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`)
3. Click **"Trigger Security Audit"**
4. Wait 30-60 seconds for analysis to complete
5. View detailed results with AI explanations

### Troubleshooting

**Check service status:**
```bash
docker compose ps
# or
docker-compose ps
```

**View logs:**
```bash
docker compose logs -f
# View specific service:
docker compose logs -f engine
```

**Restart services:**
```bash
docker compose restart
```

**Stop services:**
```bash
docker compose down
```

For more details, see [RUN.md](RUN.md) or [QUICKSTART.md](QUICKSTART.md).

---

## 🧪 Development Workflow

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Engine Development

```bash
cd engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Database Migrations

```bash
cd frontend
npx prisma migrate dev --name init
npx prisma generate
```

---

## 🔬 Technical Deep Dive

### The Audit Pipeline

1. **Contract Submission** → User submits address via Web UI
2. **Inngest Trigger** → Background job queued
3. **Source Code Fetching** → Retrieve from Etherscan/Blockscout
4. **Slither Analysis** → Static analysis detects vulnerability patterns
5. **AI Contextualization** → Gemini 1.5 Pro explains exploits in natural language
6. **Result Persistence** → Store in PostgreSQL with structured JSON
7. **Real-Time Updates** → WebSocket/polling updates UI

### Security Features

- ✅ **Reentrancy Detection** via Slither's call graph analysis
- ✅ **Access Control Flaws** (missing modifiers, public state variables)
- ✅ **Integer Overflow/Underflow** (pre-Solidity 0.8.0)
- ✅ **Unchecked External Calls** (low-level `.call()` without success checks)
- ✅ **Gas Optimization** opportunities
- ✅ **AI-Powered Exploit Chains** (multi-step vulnerability correlation)

---

## 🌐 Internationalization (i18n)

MamoruAI supports bilingual audit reports:

```json
// messages/en.json
{
  "dashboard.title": "COMMAND CENTER",
  "dashboard.subtitle": "Monitor and analyze smart contract security."
}

// messages/ja.json
{
  "dashboard.title": "コマンドセンター",
  "dashboard.subtitle": "スマートコントラクトのセキュリティを監視・分析"
}
```

Switch languages via the UI or by setting the user's locale preference.

---

## 📈 Roadmap

- [x] Core engine with Slither integration
- [x] AI-powered contextual explanations (Gemini 1.5 Pro)
- [x] Etherscan source code fetching
- [x] Database persistence for audit results
- [x] Input validation and error handling
- [x] Health check endpoints
- [x] Dockerized deployment
- [x] Basic test infrastructure
- [ ] Real-time WebSocket audit updates
- [ ] Formal verification integration (Certora/SMTChecker)
- [ ] Multi-chain support (Base, Arbitrum, Optimism - Ethereum supported)
- [ ] Public API for CI/CD integration
- [ ] Browser extension for instant contract scanning
- [ ] Comprehensive test coverage

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---



## 🙏 Acknowledgments

- **Slither** by Trail of Bits for industry-standard static analysis
- **Gemini 1.5 Pro** by Google for advanced AI reasoning
- **Inngest** for reliable background job processing
- **The Web3 Community** for building in the Zero-G environment

---

## 📞 Contact

- **Project Maintainer**: [suraj kumar]
- **Email**: surajnsg115@gmail.com
- **Twitter**: [@whotf_surajj] https://x.com/whotf_surajj

---

**Built with suraj for the decentralized future. Stay safe in Zero-G. 🚀**
