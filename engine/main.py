from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator, Field
import uvicorn
import os
import logging
from typing import Optional, Dict, List
import httpx
from dotenv import load_dotenv
from ai_service import AIService
from slither_analyzer import SlitherAnalyzer
from contract_fetcher import ContractFetcher
from utils import (
    validate_ethereum_address,
    validate_chain,
    calculate_security_score,
    extract_line_numbers_from_elements,
    sanitize_source_code,
    format_error_message
)
import time

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MamoruAI Analysis Engine",
    version="1.0.0",
    description="AI-powered smart contract security analysis engine",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for observability."""
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed after {process_time:.3f}s: {str(e)}")
        raise

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for observability."""
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed after {process_time:.3f}s: {str(e)}")
        raise

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions gracefully."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url)
        }
    )

# Initialize services
ai_service = AIService(api_key=os.getenv("GEMINI_API_KEY", ""))
slither_analyzer = SlitherAnalyzer()
contract_fetcher = ContractFetcher(etherscan_api_key=os.getenv("ETHERSCAN_API_KEY"))

class ScanRequest(BaseModel):
    contract_address: str = Field(..., description="Ethereum contract address (0x...)")
    source_code: str = Field(default="", description="Contract source code (optional if fetch_source=true)")
    bytecode: str = Field(default=None, description="Contract bytecode (optional)")
    chain: str = Field(default="ethereum", description="Blockchain network")
    fetch_source: bool = Field(default=True, description="Fetch source code from explorer if not provided")
    audit_id: Optional[str] = Field(default=None, description="Audit ID for result storage")

    @validator('contract_address')
    def validate_address(cls, v):
        if not v:
            raise ValueError("Contract address is required")
        if not validate_ethereum_address(v):
            raise ValueError("Invalid Ethereum address format. Must be 0x followed by 40 hex characters.")
        return v.lower()  # Normalize to lowercase

    @validator('chain')
    def validate_chain(cls, v):
        if not validate_chain(v):
            raise ValueError(f"Invalid chain. Supported: ethereum, base, arbitrum, optimism, polygon")
        return v.lower()

    @validator('source_code')
    def validate_source_code(cls, v):
        if v:
            return sanitize_source_code(v)
        return v

class ScanResponse(BaseModel):
    success: bool
    message: str
    address: str
    audit_id: str = None

@app.get("/")
async def root():
    return {
        "status": "MamoruAI Analysis Engine is online",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Returns detailed health status of all components.
    """
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "components": {}
    }
    
    # Check Slither
    try:
        import subprocess
        result = subprocess.run(
            ["slither", "--version"],
            capture_output=True,
            timeout=5
        )
        health_status["components"]["slither"] = {
            "available": result.returncode == 0,
            "version": result.stdout.decode().strip() if result.returncode == 0 else None
        }
    except Exception as e:
        health_status["components"]["slither"] = {
            "available": False,
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check AI Service
    ai_configured = bool(os.getenv("GEMINI_API_KEY"))
    health_status["components"]["ai_service"] = {
        "configured": ai_configured,
        "available": ai_service.model is not None if ai_configured else False
    }
    if not ai_configured:
        health_status["status"] = "degraded"
    
    # Check Frontend connectivity
    try:
        frontend_url = os.getenv("FRONTEND_URL", "http://frontend:3000")
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{frontend_url}/api/health", timeout=2.0)
            health_status["components"]["frontend"] = {
                "reachable": response.status_code < 500
            }
    except Exception as e:
        health_status["components"]["frontend"] = {
            "reachable": False,
            "error": str(e)
        }
        # Don't mark as degraded for frontend - it's not critical for engine operation
    
    return health_status

@app.post("/scan", response_model=ScanResponse)
async def trigger_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Trigger a security audit scan for a smart contract.
    If source_code is not provided and fetch_source is True, will fetch from Etherscan.
    """
    try:
        logger.info(f"Scan request received for address: {request.contract_address}")

        # Fetch source code if not provided
        source_code = request.source_code
        contract_metadata = None
        if not source_code and request.fetch_source:
            logger.info(f"Fetching source code from {request.chain} explorer")
            try:
                contract_data = await contract_fetcher.fetch_source_code(
                    request.contract_address,
                    request.chain
                )
                if contract_data:
                    source_code = contract_fetcher.normalize_source_code(contract_data)
                    contract_metadata = contract_data  # Store metadata for later
                    logger.info(f"Successfully fetched source code ({len(source_code)} chars)")
                else:
                    raise HTTPException(
                        status_code=404,
                        detail="Contract source code not found on blockchain explorer"
                    )
            except HTTPException:
                raise
            except Exception as e:
                error_msg = format_error_message(e, "Failed to fetch source code")
                logger.error(error_msg)
                raise HTTPException(
                    status_code=500,
                    detail=error_msg
                )
        
        # Store source code in database if we have audit_id and fetched it
        contract_id_for_storage = None
        if request.audit_id and contract_metadata and source_code:
            try:
                frontend_url = os.getenv("FRONTEND_URL", "http://frontend:3000")
                async with httpx.AsyncClient(timeout=10.0) as client:
                    # Get contract ID from audit
                    audit_response = await client.get(f"{frontend_url}/api/audit/{request.audit_id}")
                    if audit_response.status_code == 200:
                        audit_data = audit_response.json()
                        contract_id_for_storage = audit_data.get("contractId")
                        if not contract_id_for_storage and audit_data.get("contract"):
                            contract_id_for_storage = audit_data["contract"].get("id")
                        if contract_id_for_storage:
                            # Update contract with source code
                            update_response = await client.put(
                                f"{frontend_url}/api/contract/{contract_id_for_storage}",
                                json={
                                    "sourceCode": source_code,
                                    "name": contract_metadata.get("contractName"),
                                },
                            )
                            if update_response.status_code == 200:
                                logger.info(f"Source code stored for contract {contract_id_for_storage}")
            except Exception as e:
                logger.warning(f"Failed to store source code in database: {str(e)}")
                # Don't fail the scan if source code storage fails

        if not source_code:
            raise HTTPException(
                status_code=400,
                detail="Source code is required. Provide source_code or set fetch_source=true"
            )

        # Run analysis in background
        background_tasks.add_task(
            perform_analysis,
            request.contract_address,
            source_code,
            request.chain,
            request.audit_id,  # Pass audit_id for result storage
            contract_metadata  # Pass metadata for contract info
        )

        return ScanResponse(
            success=True,
            message="Scan triggered successfully",
            address=request.contract_address
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = format_error_message(e, "Error triggering scan")
        logger.error(error_msg, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please check logs for details."
        )

async def perform_analysis(
    contract_address: str, 
    source_code: str, 
    chain: str, 
    audit_id: Optional[str] = None,
    contract_metadata: Optional[Dict] = None
):
    """
    Perform the actual security analysis:
    1. Run Slither static analysis
    2. Send results to AI for contextualization
    3. Store results via API call to frontend
    """
    try:
        logger.info(f"Starting analysis for {contract_address}")

        # Step 1: Run Slither analysis
        logger.info("Running Slither static analysis...")
        slither_results = slither_analyzer.analyze_contract(source_code)
        logger.info(f"Slither found {slither_results['statistics']['total_vulnerabilities']} vulnerabilities")

        # Step 2: Get AI contextualization
        logger.info("Sending results to AI for contextualization...")
        ai_report = None
        try:
            ai_report = await ai_service.analyze_report(contract_address, slither_results)
            logger.info("AI analysis completed")
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            # Continue without AI report if it fails
            ai_report = "AI analysis unavailable. See Slither results below."

        # Step 3: Calculate security score (0-100)
        stats = slither_results['statistics']
        total_vulns = stats['total_vulnerabilities']
        critical = stats['critical']
        high = stats['high']
        medium = stats['medium']
        
        # Use utility function for score calculation
        score = calculate_security_score(stats)

        # Prepare final results
        results = {
            "contract_address": contract_address,
            "chain": chain,
            "score": score,
            "statistics": stats,
            "vulnerabilities": slither_results['vulnerabilities'],
            "ai_report": ai_report,
            "slither_raw": slither_results.get('raw_output', {}),
            "source_code_length": len(source_code)
        }

        logger.info(f"Analysis completed for {contract_address}. Score: {score}/100")

        # Step 4: Store results in database via frontend API
        if audit_id:
            try:
                frontend_url = os.getenv("FRONTEND_URL", "http://frontend:3000")
                async with httpx.AsyncClient(timeout=30.0) as client:
                    # Prepare vulnerability data with improved line number extraction
                    vulnerabilities_data = []
                    for v in slither_results['vulnerabilities']:
                        elements = v.get("elements", [])
                        line_numbers = extract_line_numbers_from_elements(elements)
                        
                        vulnerabilities_data.append({
                            "type": v.get("type", "Unknown"),
                            "severity": v.get("severity", "LOW"),
                            "description": v.get("description", "") or v.get("markdown", ""),
                            "lineNumbers": line_numbers,
                            "location": v.get("first_markdown_element", ""),
                            "markdown": v.get("markdown", ""),
                            "confidence": v.get("confidence", "Unknown"),
                        })
                    
                    response = await client.put(
                        f"{frontend_url}/api/audit/{audit_id}",
                        json={
                            "status": "COMPLETED",
                            "score": score,
                            "summary": f"Found {total_vulns} vulnerabilities: {critical} critical, {high} high, {medium} medium, {stats['low']} low",
                            "detailReport": ai_report,
                            "slitherRaw": slither_results.get('raw_output', {}),
                            "vulnerabilities": vulnerabilities_data,
                        },
                    )
                    if response.status_code == 200:
                        logger.info(f"Results stored successfully for audit {audit_id}")
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to store results: {response.status_code} - {error_text}")
                        raise Exception(f"Failed to store results: {response.status_code}")
            except Exception as e:
                logger.error(f"Error storing results in database: {str(e)}")
                # Try to mark audit as failed
                try:
                    frontend_url = os.getenv("FRONTEND_URL", "http://frontend:3000")
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        await client.put(
                            f"{frontend_url}/api/audit/{audit_id}",
                            json={"status": "FAILED"},
                        )
                except:
                    pass
                raise  # Re-raise to trigger error handling

        return results

    except Exception as e:
        error_msg = format_error_message(e, "Error during analysis")
        logger.error(error_msg, exc_info=True)
        
        # Try to update audit status to FAILED if we have audit_id
        if audit_id:
            try:
                frontend_url = os.getenv("FRONTEND_URL", "http://frontend:3000")
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.put(
                        f"{frontend_url}/api/audit/{audit_id}",
                        json={
                            "status": "FAILED",
                            "summary": f"Analysis failed: {str(e)[:200]}"
                        },
                    )
            except Exception as update_error:
                logger.error(f"Failed to update audit status: {str(update_error)}")
        
        raise


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
