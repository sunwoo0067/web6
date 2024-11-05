from typing import Dict, List, Optional
import httpx
from app.core.config import settings

class ZenTradeAPI:
    def __init__(self):
        self.base_url = settings.ZENTRADE_API_URL
        self.api_id = settings.ZENTRADE_API_ID
        self.api_key = settings.ZENTRADE_API_KEY
        
    async def _make_request(self, params: Dict) -> Dict:
        """API 요청 공통 메서드"""
        base_params = {
            "id": self.api_id,
            "m_key": self.api_key
        }
        params.update(base_params)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_products(self, page: int = 1) -> List[Dict]:
        """상품 목록 조회"""
        params = {
            "mode": "goods_list",
            "page": page
        }
        return await self._make_request(params)
    
    async def get_product_detail(self, product_id: str) -> Dict:
        """상품 상세 정보 조회"""
        params = {
            "mode": "goods_detail",
            "goods_id": product_id
        }
        return await self._make_request(params)
    
    async def get_orders(self, start_date: str, end_date: str) -> List[Dict]:
        """주문 목록 조회"""
        params = {
            "mode": "order_list",
            "start_date": start_date,
            "end_date": end_date
        }
        return await self._make_request(params) 