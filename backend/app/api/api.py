from fastapi import APIRouter
from app.api.endpoints import users, auth, profiles, posts, files

api_router = APIRouter()

api_router.include_router(
    auth.router,
    tags=["auth"],
    prefix="/auth"
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    profiles.router,
    prefix="/profiles",
    tags=["profiles"]
)

api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"]
)

api_router.include_router(
    files.router,
    prefix="/files",
    tags=["files"]
)
