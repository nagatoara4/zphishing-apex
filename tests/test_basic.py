"""Basic tests for ZPHISHING APEX"""

import pytest

def test_import():
    """Test that main module can be imported"""
    try:
        import zphishing
        assert True
    except ImportError:
        pytest.fail("Failed to import zphishing")

def test_version():
    """Test version is defined"""
    import zphishing
    assert hasattr(zphishing, '__version__')
    assert zphishing.__version__ == "4.0.0"

if __name__ == "__main__":
    pytest.main([__file__])
