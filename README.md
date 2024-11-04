# web6
# 위탁 판매 자동화 시스템 개발 프롬프트

위탁 판매 자동화 시스템의 첫 단계 개발을 시작하려고 합니다. FastAPI를 사용하여 백엔드를 구축하고, Vue.js로 프론트엔드를 개발하려고 합니다. 네이버 클라우드 플랫폼을 인프라로 사용할 예정입니다.

## 1단계: 프로젝트 초기 설정

다음 구조로 프로젝트를 설정해주세요:

```
consignment-system/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── core/        # 설정, 유틸리티
│   │   ├── api/         # API 라우트
│   │   ├── models/      # 데이터베이스 모델
│   │   ├── schemas/     # Pydantic 스키마
│   │   └── services/    # 비즈니스 로직
│   ├── tests/           # 테스트 코드
│   └── requirements.txt
├── frontend/            # Vue.js 프론트엔드
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── store/
│   │   └── api/
│   └── package.json
└── docker-compose.yml   # 개발 환경 설정
```

### 기술 스택 상세:
- Backend: FastAPI, SQLAlchemy, Celery
- Frontend: Vue.js 3, Vuex, Vue Router
- Database: MySQL
- Cache: Redis
- Image Processing: Pillow, rembg
- Infrastructure: 네이버 클라우드 플랫폼

## 2단계: 핵심 기능 구현

다음 순서로 핵심 기능을 구현해주세요:

1. **상품 수집 모듈**
```python
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

class ProductCollector:
    def __init__(self, wholesale_api_key: str):
        self.api_key = wholesale_api_key
        
    async def search_products(self, keyword: str) -> List[dict]:
        """도매 사이트 상품 검색"""
        pass
        
    async def get_product_details(self, product_id: str) -> dict:
        """상품 상세 정보 수집"""
        pass
        
    async def download_images(self, image_urls: List[str]) -> List[str]:
        """상품 이미지 다운로드"""
        pass

class ImageProcessor:
    async def process_images(self, image_paths: List[str]) -> List[str]:
        """
        이미지 처리 파이프라인:
        1. 배경 제거
        2. 좌우반전
        3. 텍스트 제거
        4. 대표 이미지 선정
        """
        pass
```

2. **이미지 처리 모듈 상세 구현 필요**:
- 배경 제거, 이미지 편집 등의 세부 기능을 구현해주세요.
- 이미지 처리 결과를 네이버 클라우드 Object Storage에 저장하는 로직을 포함해주세요.

3. **상품 등록 자동화 모듈**:
- 각 오픈마켓별 API 연동
- 상품명 최적화 로직
- 대량 등록 처리

4. **주문/재고 관리 모듈**:
- 실시간 재고 확인
- 자동 발주 시스템
- 상태 업데이트 자동화

## 3단계: 데이터베이스 스키마

다음 테이블 구조로 데이터베이스를 설계해주세요:

```sql
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    wholesale_id VARCHAR(100),
    name VARCHAR(200),
    original_name VARCHAR(200),
    price DECIMAL(10,2),
    wholesale_price DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE product_images (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36),
    image_url VARCHAR(500),
    is_representative BOOLEAN,
    processing_status VARCHAR(20),
    created_at TIMESTAMP
);

CREATE TABLE marketplace_products (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36),
    marketplace_id VARCHAR(36),
    marketplace_product_id VARCHAR(100),
    status VARCHAR(20),
    created_at TIMESTAMP
);
```

## 4단계: API 엔드포인트 구현

다음 API 엔드포인트를 구현해주세요:

```python
@router.post("/products/search")
async def search_products(
    keyword: str,
    wholesale_id: str,
    db: Session = Depends(get_db)
):
    """도매 상품 검색"""
    pass

@router.post("/products/register")
async def register_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    """상품 등록"""
    pass

@router.post("/products/upload-marketplace")
async def upload_to_marketplace(
    product_id: str,
    marketplace_ids: List[str],
    db: Session = Depends(get_db)
):
    """오픈마켓 상품 등록"""
    pass
```

## 5단계: 백그라운드 작업 처리

Celery를 사용하여 다음 작업을 구현해주세요:

```python
@celery_app.task
async def process_product_images(product_id: str):
    """이미지 처리 작업"""
    pass

@celery_app.task
async def sync_inventory():
    """재고 동기화 작업"""
    pass

@celery_app.task
async def update_marketplace_status():
    """오픈마켓 상태 업데이트"""
    pass
```

## 6단계: 프론트엔드 구현

Vue.js 컴포넌트 구조:

```vue
<!-- ProductSearch.vue -->
<template>
  <div>
    <!-- 상품 검색 폼 -->
    <!-- 검색 결과 목록 -->
    <!-- 상품 등록 버튼 -->
  </div>
</template>

<!-- ProductList.vue -->
<template>
  <div>
    <!-- 등록된 상품 목록 -->
    <!-- 상태 필터링 -->
    <!-- 일괄 작업 버튼 -->
  </div>
</template>
```

## 추가 요구사항:

1. **에러 처리**:
- API 요청 실패 시 재시도 로직
- 이미지 처리 실패 시 복구 메커니즘
- 로깅 시스템 구축

2. **성능 최적화**:
- 이미지 처리 병렬화
- 데이터베이스 인덱싱
- 캐싱 전략

3. **모니터링**:
- API 응답 시간 모니터링
- 에러 발생 알림
- 리소스 사용량 추적

각 단계별로 구현하면서, 테스트 코드도 함께 작성해주세요. 특히 이미지 처리와 API 연동 부분은 단위 테스트가 중요합니다.

먼저 어떤 부분부터 구현을 시작하면 좋을까요?
