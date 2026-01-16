import httpx
import os
import json
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ContractFetcher:
    def __init__(self, etherscan_api_key: Optional[str] = None):
        self.etherscan_api_key = etherscan_api_key or os.getenv("ETHERSCAN_API_KEY", "")
        self.base_urls = {
            "ethereum": "https://api.etherscan.io/api",
            "base": "https://api.basescan.org/api",
            "arbitrum": "https://api.arbiscan.io/api",
            "optimism": "https://api-optimistic.etherscan.io/api",
        }

    async def fetch_source_code(self, address: str, chain: str = "ethereum") -> Optional[Dict]:
        """
        Fetch contract source code from blockchain explorer.
        Returns dict with sourceCode, contractName, compilerVersion, etc.
        """
        if not address or not address.startswith("0x"):
            raise ValueError("Invalid contract address format")

        base_url = self.base_urls.get(chain.lower(), self.base_urls["ethereum"])
        
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": self.etherscan_api_key if self.etherscan_api_key else "YourApiKeyToken"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("result"):
                    result = data["result"][0]
                    
                    # Handle case where source code might be in a JSON string
                    source_code = result.get("SourceCode", "")
                    if source_code.startswith("{{"):
                        # Multi-file contract (flattened JSON)
                        try:
                            source_code = json.loads(source_code)
                        except json.JSONDecodeError:
                            pass
                    elif source_code.startswith("{"):
                        # Single file JSON
                        try:
                            parsed = json.loads(source_code)
                            if isinstance(parsed, dict) and "sources" in parsed:
                                # Standard JSON format
                                source_code = parsed
                        except json.JSONDecodeError:
                            pass

                    return {
                        "sourceCode": source_code,
                        "contractName": result.get("ContractName", ""),
                        "compilerVersion": result.get("CompilerVersion", ""),
                        "optimizationUsed": result.get("OptimizationUsed", "0") == "1",
                        "runs": int(result.get("Runs", 0)),
                        "constructorArguments": result.get("ConstructorArguments", ""),
                        "evmVersion": result.get("EVMVersion", ""),
                        "library": result.get("Library", ""),
                        "licenseType": result.get("LicenseType", ""),
                        "proxy": result.get("Proxy", "0") == "1",
                        "implementation": result.get("Implementation", ""),
                        "swarmSource": result.get("SwarmSource", ""),
                    }
                else:
                    return None
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching contract {address} from {chain}")
            raise Exception("Timeout fetching contract source code. The explorer API may be slow or unavailable.")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code} error fetching contract {address}")
            if e.response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again later.")
            raise Exception(f"HTTP error fetching contract: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching contract {address}: {str(e)}")
            raise Exception(f"Error fetching contract source code: {str(e)}")

    def normalize_source_code(self, source_data: Dict) -> str:
        """
        Normalize source code from various formats to a single string.
        Handles single file, multi-file, and JSON formats.
        """
        source_code = source_data.get("sourceCode", "")
        
        if isinstance(source_code, str):
            return source_code
        elif isinstance(source_code, dict):
            # Multi-file contract - combine all files
            if "sources" in source_code:
                combined = []
                for file_path, file_data in source_code["sources"].items():
                    if isinstance(file_data, dict) and "content" in file_data:
                        combined.append(f"// File: {file_path}\n{file_data['content']}\n")
                    elif isinstance(file_data, str):
                        combined.append(f"// File: {file_path}\n{file_data}\n")
                return "\n".join(combined)
        
        return str(source_code)
