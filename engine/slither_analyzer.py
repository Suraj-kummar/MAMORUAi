import subprocess
import json
import tempfile
import os
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class SlitherAnalyzer:
    def __init__(self, timeout: int = 120):
        """
        Initialize Slither analyzer.
        
        Args:
            timeout: Maximum time in seconds for Slither analysis (default: 120)
        """
        self.timeout = timeout
        self.max_source_size = 500000  # 500KB max source code size

    def analyze_contract(self, source_code: str, contract_name: Optional[str] = None) -> Dict:
        """
        Run Slither analysis on contract source code.
        Returns parsed JSON results with vulnerabilities.
        """
        if not source_code or not source_code.strip():
            raise ValueError("Source code cannot be empty")
        
        # Check source code size
        if len(source_code) > self.max_source_size:
            logger.warning(f"Source code is large ({len(source_code)} chars), analysis may be slow")

        # Create temporary file for contract
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as temp_file:
            temp_file.write(source_code)
            temp_path = temp_file.name

        try:
            # Run Slither analysis
            cmd = [
                "slither",
                temp_path,
                "--json",
                "-"
            ]

            if contract_name:
                cmd.extend(["--contract-name", contract_name])

            logger.info(f"Running Slither analysis on {temp_path}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=os.path.dirname(temp_path)
            )

            if result.returncode != 0:
                logger.warning(f"Slither returned non-zero exit code: {result.returncode}")
                logger.warning(f"Stderr: {result.stderr}")
                # Slither may still produce valid output even with non-zero exit code
                if not result.stdout:
                    raise Exception(f"Slither analysis failed: {result.stderr}")

            # Parse JSON output
            try:
                # Slither outputs JSON to stdout
                output_lines = result.stdout.strip().split('\n')
                json_output = None
                
                # Find JSON object in output (may have warnings before it)
                for line in output_lines:
                    line = line.strip()
                    if line.startswith('{'):
                        json_output = json.loads(line)
                        break
                
                if not json_output:
                    # Try parsing entire stdout
                    json_output = json.loads(result.stdout)

                return self._parse_slither_output(json_output)

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Slither JSON output: {e}")
                logger.error(f"Output: {result.stdout[:500]}")
                raise Exception(f"Failed to parse Slither output: {str(e)}")

        except subprocess.TimeoutExpired:
            raise Exception(f"Slither analysis timed out after {self.timeout} seconds")
        except Exception as e:
            logger.error(f"Error running Slither: {str(e)}")
            raise
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

    def _parse_slither_output(self, slither_json: Dict) -> Dict:
        """
        Parse and structure Slither JSON output into our format.
        """
        detectors = slither_json.get("results", {}).get("detectors", [])
        
        vulnerabilities = []
        for detector in detectors:
            if detector.get("check") and detector.get("impact") and detector.get("confidence"):
                vulnerabilities.append({
                    "type": detector.get("check", "Unknown"),
                    "severity": self._map_severity(detector.get("impact", "Informational")),
                    "confidence": detector.get("confidence", "Unknown"),
                    "description": detector.get("description", ""),
                    "markdown": detector.get("markdown", ""),
                    "elements": detector.get("elements", []),
                    "first_markdown_element": detector.get("first_markdown_element", ""),
                })

        # Extract contract information
        contracts = slither_json.get("results", {}).get("contracts", [])
        
        return {
            "success": True,
            "vulnerabilities": vulnerabilities,
            "contracts": contracts,
            "statistics": {
                "total_vulnerabilities": len(vulnerabilities),
                "critical": len([v for v in vulnerabilities if v["severity"] == "CRITICAL"]),
                "high": len([v for v in vulnerabilities if v["severity"] == "HIGH"]),
                "medium": len([v for v in vulnerabilities if v["severity"] == "MEDIUM"]),
                "low": len([v for v in vulnerabilities if v["severity"] == "LOW"]),
            },
            "raw_output": slither_json
        }

    def _map_severity(self, slither_impact: str) -> str:
        """Map Slither impact levels to our severity enum."""
        mapping = {
            "High": "CRITICAL",
            "Medium": "HIGH",
            "Low": "MEDIUM",
            "Informational": "LOW",
            "Optimization": "INFORMATIONAL",
        }
        return mapping.get(slither_impact, "LOW")
