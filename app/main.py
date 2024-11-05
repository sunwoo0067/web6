from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint"}

@app.get("/api/items")
async def read_items():
    return [
        {"id": 1, "name": "Item One"},
        {"id": 2, "name": "Item Two"}
    ]

@app.get("/api/items/{item_id}")
async def read_item(item_id: int):
    items = [
        {"id": 1, "name": "Item One"},
        {"id": 2, "name": "Item Two"}
    ]
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return item
    return {"error": "Item not found"} 