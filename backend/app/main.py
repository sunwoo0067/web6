from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Backend!"}

@app.get("/health-check")
def health_check():
    return {"status": "healthy"}
