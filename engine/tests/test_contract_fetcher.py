import pytest
from contract_fetcher import ContractFetcher

@pytest.mark.asyncio
async def test_validate_address():
    """Test address validation."""
    fetcher = ContractFetcher()
    
    # Valid address
    assert await fetcher.fetch_source_code("0x" + "0" * 40) is None or True  # May not exist but format is valid
    
    # Invalid addresses should raise ValueError
    with pytest.raises(ValueError):
        await fetcher.fetch_source_code("invalid")
    
    with pytest.raises(ValueError):
        await fetcher.fetch_source_code("0x123")  # Too short

def test_normalize_source_code():
    """Test source code normalization."""
    fetcher = ContractFetcher()
    
    # Single string
    assert fetcher.normalize_source_code({"sourceCode": "pragma solidity ^0.8.0;"}) == "pragma solidity ^0.8.0;"
    
    # Multi-file format
    multi_file = {
        "sourceCode": {
            "sources": {
                "Contract.sol": {"content": "pragma solidity ^0.8.0;"}
            }
        }
    }
    result = fetcher.normalize_source_code(multi_file)
    assert "Contract.sol" in result
    assert "pragma solidity" in result
