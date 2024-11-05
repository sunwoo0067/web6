from celery import Celery
from app.core.external_api.zentrade import ZenTradeAPI
from app.db.session import SessionLocal

celery_app = Celery("worker", broker="redis://localhost:6379/0")

@celery_app.task
async def sync_zentrade_products():
    """젠트레이드 상품 정보 동기화 (매일 실행)"""
    api = ZenTradeAPI()
    db = SessionLocal()
    
    try:
        page = 1
        while True:
            products = await api.get_products(page)
            if not products:
                break
                
            # 상품 정보 업데이트
            for product_data in products:
                # ... 상품 정보 처리 로직 ...
                
            page += 1
            
    finally:
        db.close() 