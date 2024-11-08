from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS 설정
=======
from app.api.api import api_router
from app.core.config import settings

description = """
FastAPI Backend API 

## Users
* Create and manage users
* Manage profile information

## Authentication
* JWT token based authentication
* Access token and refresh token support

## Posts
* CRUD operations for posts
* User-specific post management

## Files
* File upload and management
* User-specific file listing
"""

app = FastAPI(
    title="FastAPI Backend",
    description=description,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Your Name",
        "url": "http://example.com/contact/",
        "email": "your@email.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# CORS settings
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
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
=======
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend!"}

@app.get("/health-check")
def health_check():
    return {"status": "healthy"}
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
