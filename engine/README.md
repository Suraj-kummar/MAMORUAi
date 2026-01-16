# MamoruAI Analysis Engine

Python FastAPI service for smart contract security analysis using Slither and Gemini AI.

## Features

- **Slither Integration**: Static analysis of Solidity contracts
- **AI Contextualization**: Gemini 1.5 Pro explains vulnerabilities
- **Source Code Fetching**: Automatic retrieval from Etherscan/Blockscout
- **Multi-chain Support**: Ethereum, Base, Arbitrum, Optimism

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_key"
export ETHERSCAN_API_KEY="your_key"
export FRONTEND_URL="http://frontend:3000"

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### `POST /scan`
Trigger a security audit scan.

**Request:**
```json
{
  "contract_address": "0x...",
  "fetch_source": true,
  "chain": "ethereum",
  "audit_id": "optional_audit_id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Scan triggered successfully",
  "address": "0x..."
}
```

### `GET /health`
Health check endpoint.

## Testing

```bash
pytest tests/
```

## Architecture

1. Receives scan request with contract address
2. Fetches source code from blockchain explorer (if needed)
3. Runs Slither static analysis
4. Sends results to Gemini AI for contextualization
5. Stores results in database via frontend API
6. Returns analysis results
