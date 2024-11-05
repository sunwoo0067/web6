import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.main import app
from tests.mock_data.zentrade_responses import MOCK_PRODUCT_LIST

client = TestClient(app)

def test_fetch_zentrade_products_success():
    with patch('app.core.external_api.zentrade.ZenTradeAPI.get_products') as mock_get_products:
        # Mock the API response
        mock_get_products.return_value = MOCK_PRODUCT_LIST

        # Make request to endpoint
        response = client.get("/api/v1/zentrade/products?page=1")

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["external_id"] == "12345"
        assert data[0]["name"] == "테스트 상품 1"

def test_fetch_zentrade_products_error():
    with patch('app.core.external_api.zentrade.ZenTradeAPI.get_products') as mock_get_products:
        # Mock an API error
        mock_get_products.side_effect = Exception("API Error")

        # Make request to endpoint
        response = client.get("/api/v1/zentrade/products?page=1")

        # Verify error response
        assert response.status_code == 500
        assert response.json()["detail"] == "API Error" 