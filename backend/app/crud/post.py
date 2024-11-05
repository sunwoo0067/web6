from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post.model_dump().items():
            setattr(db_post, key, value)
        db_post.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
