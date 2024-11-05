import pytest
from unittest.mock import patch, Mock
from httpx import Response
import json

from app.core.external_api.zentrade import ZenTradeAPI
from tests.mock_data.zentrade_responses import MOCK_PRODUCT_LIST, MOCK_PRODUCT_DETAIL

@pytest.fixture
def zentrade_api():
    return ZenTradeAPI()

@pytest.mark.asyncio
async def test_get_products_success(zentrade_api):
    # Mock the httpx client response
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_PRODUCT_LIST
        mock_get.return_value = mock_response

        # Call the API
        products = await zentrade_api.get_products(page=1)

        # Verify the response
        assert products == MOCK_PRODUCT_LIST
        assert len(products["products"]) == 2
        assert products["products"][0]["goods_id"] == "12345"

@pytest.mark.asyncio
async def test_get_product_detail_success(zentrade_api):
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_PRODUCT_DETAIL
        mock_get.return_value = mock_response

        # Call the API
        product = await zentrade_api.get_product_detail("12345")

        # Verify the response
        assert product == MOCK_PRODUCT_DETAIL
        assert product["product"]["goods_id"] == "12345"

@pytest.mark.asyncio
async def test_api_error_handling(zentrade_api):
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = Mock(spec=Response)
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        # Test error handling
        with pytest.raises(Exception) as exc_info:
            await zentrade_api.get_products()
        assert str(exc_info.value) == "API Error" 