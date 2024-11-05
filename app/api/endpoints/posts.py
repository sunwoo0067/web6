from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import post as post_crud
from app.schemas.post import Post, PostCreate, PostUpdate
from app.core.security import get_current_user_from_token
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    return post_crud.create_post(db, post, current_user_id)

@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = post_crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/", response_model=List[Post])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    posts = post_crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.put("/{post_id}", response_model=Post)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    db_post = post_crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return post_crud.update_post(db, post_id, post)

@router.delete("/{post_id}", response_model=Post)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    db_post = post_crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return post_crud.delete_post(db, post_id)
