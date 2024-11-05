MOCK_PRODUCT_LIST = {
    "result": "success",
    "products": [
        {
            "goods_id": "12345",
            "goods_name": "테스트 상품 1",
            "price": "15000",
            "supply_price": "10000",
            "goods_detail": "상품 상세 설명입니다.",
            "image_urls": ["http://example.com/image1.jpg"],
            "brand": "테스트 브랜드",
            "category": "의류",
            "stock": "100"
        },
        {
            "goods_id": "12346",
            "goods_name": "테스트 상품 2",
            "price": "25000",
            "supply_price": "18000",
            "goods_detail": "두 번째 상품 설명입니다.",
            "image_urls": ["http://example.com/image2.jpg"],
            "brand": "테스트 브랜드2",
            "category": "잡화",
            "stock": "50"
        }
    ]
}

MOCK_PRODUCT_DETAIL = {
    "result": "success",
    "product": {
        "goods_id": "12345",
        "goods_name": "테스트 상품 1",
        "price": "15000",
        "supply_price": "10000",
        "goods_detail": "상품 상세 설명입니다.",
        "image_urls": ["http://example.com/image1.jpg"],
        "brand": "테스트 브랜드",
        "category": "의류",
        "stock": "100",
        "options": [
            {"option_name": "색상", "option_value": "빨강"},
            {"option_name": "사이즈", "option_value": "M"}
        ]
    }
} 