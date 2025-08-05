import pytest
from unittest.mock import patch, MagicMock
import json
import httpx
from llm_openrouter import (
    get_openrouter_models, 
    fetch_cached_json, 
    get_supports_images, 
    format_pricing, 
    format_price,
    DownloadError
)

def test_get_openrouter_models_with_none_data():
    """Test get_openrouter_models when fetch_cached_json returns None data."""
    with patch('llm_openrouter.fetch_cached_json') as mock_fetch:
        # Mock fetch_cached_json to return None data
        mock_fetch.side_effect = [
            {"data": None},  # First call for models
            {"data": []}     # Second call for schema supporting models
        ]
        
        # This should not raise an exception
        models = get_openrouter_models()
        assert models == []

def test_get_openrouter_models_with_missing_data_key():
    """Test get_openrouter_models when fetch_cached_json returns missing data key."""
    with patch('llm_openrouter.fetch_cached_json') as mock_fetch:
        # Mock fetch_cached_json to return missing data key
        mock_fetch.side_effect = [
            {},  # First call for models
            {}   # Second call for schema supporting models
        ]
        
        # This should not raise an exception
        models = get_openrouter_models()
        assert models == []

def test_fetch_cached_json_with_none_return():
    """Test fetch_cached_json when json.load returns None."""
    with patch('llm_openrouter.Path') as mock_path, \
         patch('llm_openrouter.open') as mock_open, \
         patch('llm_openrouter.json.load') as mock_json_load, \
         patch('llm_openrouter.httpx.get') as mock_get:
        
        # Mock path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = True
        mock_path_instance.stat().st_mtime = 0  # Force cache timeout
        
        # Mock json.load to return None
        mock_json_load.return_value = None
        
        # Mock httpx.get to return valid data
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        # This should not raise an exception and should return the HTTP data
        result = fetch_cached_json("http://test.com", "/test/path", 0)
        assert result == {"test": "data"}

def test_fetch_cached_json_with_http_error_and_none_file():
    """Test fetch_cached_json when HTTP fails and file loading returns None."""
    with patch('llm_openrouter.Path') as mock_path, \
         patch('llm_openrouter.open') as mock_open, \
         patch('llm_openrouter.json.load') as mock_json_load, \
         patch('llm_openrouter.httpx.get') as mock_get:
        
        # Mock path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.is_file.return_value = True
        mock_path_instance.stat().st_mtime = 0  # Force cache timeout
        
        # Mock json.load to return None
        mock_json_load.return_value = None
        
        # Mock httpx.get to raise HTTPError
        mock_get.side_effect = httpx.HTTPError("Test error")
        
        # This should raise DownloadError
        with pytest.raises(DownloadError):
            fetch_cached_json("http://test.com", "/test/path", 0)

def test_get_supports_images_with_none_model_definition():
    """Test get_supports_images with None model_definition."""
    result = get_supports_images(None)
    assert result is False

def test_get_supports_images_with_missing_architecture():
    """Test get_supports_images with missing architecture key."""
    model_definition = {}
    result = get_supports_images(model_definition)
    assert result is False

def test_get_supports_images_with_none_architecture():
    """Test get_supports_images with None architecture."""
    model_definition = {"architecture": None}
    result = get_supports_images(model_definition)
    assert result is False

def test_get_supports_images_with_missing_modality():
    """Test get_supports_images with missing modality key."""
    model_definition = {"architecture": {}}
    result = get_supports_images(model_definition)
    assert result is False

def test_get_supports_images_with_none_modality():
    """Test get_supports_images with None modality."""
    model_definition = {"architecture": {"modality": None}}
    result = get_supports_images(model_definition)
    assert result is False

def test_format_pricing_with_none_dict():
    """Test format_pricing with None pricing_dict."""
    result = format_pricing(None)
    assert result == ""

def test_format_price_with_none_price_str():
    """Test format_price with None price_str."""
    result = format_price("test", None)
    assert result is None

def test_format_price_with_invalid_price_str():
    """Test format_price with invalid price_str."""
    result = format_price("test", "invalid")
    assert result is None

if __name__ == "__main__":
    pytest.main([__file__])