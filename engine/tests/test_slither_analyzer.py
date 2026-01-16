import pytest
from slither_analyzer import SlitherAnalyzer

def test_analyze_empty_source():
    """Test that empty source code raises error."""
    analyzer = SlitherAnalyzer()
    
    with pytest.raises(ValueError):
        analyzer.analyze_contract("")

def test_severity_mapping():
    """Test severity level mapping."""
    analyzer = SlitherAnalyzer()
    
    assert analyzer._map_severity("High") == "CRITICAL"
    assert analyzer._map_severity("Medium") == "HIGH"
    assert analyzer._map_severity("Low") == "MEDIUM"
    assert analyzer._map_severity("Informational") == "LOW"
    assert analyzer._map_severity("Unknown") == "LOW"  # Default
