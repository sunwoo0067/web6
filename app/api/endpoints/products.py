from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.core.external_api.zentrade import ZenTradeAPI
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.crud import product as product_crud

router = APIRouter()

@router.get("/zentrade/products", response_model=List[Product])
async def fetch_zentrade_products(
    page: int = 1,
    db: Session = Depends(get_db)
):
    """젠트레이드 상품 목록 수집"""
    try:
        api = ZenTradeAPI()
        products = await api.get_products(page)
        
        # 수집한 상품 데이터를 DB에 저장
        saved_products = []
        for product_data in products:
            product = ProductCreate(
                source="zentrade",
                external_id=str(product_data["goods_id"]),
                name=product_data["goods_name"],
                price=float(product_data["price"]),
                wholesale_price=float(product_data["supply_price"]),
                description=product_data.get("goods_detail", ""),
                image_urls=product_data.get("image_urls", []),
                brand=product_data.get("brand", ""),
                category=product_data.get("category", ""),
                stock=int(product_data.get("stock", 0))
            )
            saved_products.append(product_crud.create_product(db, product))
            
        return saved_products
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 