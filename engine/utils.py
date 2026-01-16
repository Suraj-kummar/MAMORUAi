"""
Utility functions for the analysis engine.
"""
import re
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

def validate_ethereum_address(address: str) -> bool:
    """Validate Ethereum address format."""
    if not address:
        return False
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))

def validate_chain(chain: str) -> bool:
    """Validate chain name."""
    valid_chains = ["ethereum", "base", "arbitrum", "optimism", "polygon"]
    return chain.lower() in valid_chains

def calculate_security_score(stats: Dict) -> int:
    """
    Calculate security score (0-100) based on vulnerability statistics.
    Higher score = more secure.
    """
    critical = stats.get('critical', 0)
    high = stats.get('high', 0)
    medium = stats.get('medium', 0)
    low = stats.get('low', 0)
    informational = stats.get('informational', 0)
    
    # Penalty weights
    base_score = 100
    score = base_score
    score -= critical * 30  # Critical vulnerabilities heavily penalize
    score -= high * 15       # High severity significant penalty
    score -= medium * 5      # Medium severity moderate penalty
    score -= low * 1         # Low severity minor penalty
    score -= informational * 0.1  # Informational almost no penalty
    
    return max(0, min(100, int(score)))  # Clamp between 0-100

def extract_line_numbers_from_elements(elements: List[Dict]) -> List[int]:
    """
    Extract line numbers from Slither vulnerability elements.
    More robust parsing of source mappings.
    """
    line_numbers = []
    
    for element in elements:
        if not isinstance(element, dict):
            continue
            
        # Try multiple ways to get line numbers
        source_mapping = element.get("source_mapping")
        if source_mapping:
            # Format: "start:length:file_id" or "start:length"
            parts = str(source_mapping).split(":")
            if len(parts) >= 1:
                try:
                    # Start position - approximate line number (rough estimate)
                    start_pos = int(parts[0])
                    # Rough estimate: assume ~80 chars per line
                    line_num = max(1, start_pos // 80)
                    if line_num not in line_numbers:
                        line_numbers.append(line_num)
                except (ValueError, TypeError):
                    pass
        
        # Also check for explicit line numbers
        if "line" in element:
            try:
                line_num = int(element["line"])
                if line_num not in line_numbers:
                    line_numbers.append(line_num)
            except (ValueError, TypeError):
                pass
    
    # Sort and limit
    line_numbers.sort()
    return line_numbers[:20]  # Limit to first 20 line numbers

def sanitize_source_code(source_code: str, max_length: int = 1000000) -> str:
    """
    Sanitize source code input.
    Remove potentially dangerous content and limit size.
    """
    if not source_code:
        return ""
    
    # Limit length
    if len(source_code) > max_length:
        logger.warning(f"Source code truncated from {len(source_code)} to {max_length} chars")
        source_code = source_code[:max_length]
    
    # Remove null bytes
    source_code = source_code.replace('\x00', '')
    
    return source_code

def format_error_message(error: Exception, context: str = "") -> str:
    """Format error message with context."""
    error_msg = str(error)
    if context:
        return f"{context}: {error_msg}"
    return error_msg
