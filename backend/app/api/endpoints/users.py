from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from app.crud import user as user_crud
from app.db.session import get_db
from app.schemas.user import User, UserCreate

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - **email**: Valid email address (required)
    - **username**: Username (required)
    - **password**: Password (required)

    Returns 400 error if email already exists.
    """
    logger.info(f"Attempting to create user with email: {user.email}")
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"User with email {user.email} already exists")
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return user_crud.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of users.

    - **skip**: Number of records to skip (optional, default: 0)
    - **limit**: Maximum number of records to return (optional, default: 100)
    """
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user information by ID.

    - **user_id**: ID of the user to retrieve (required)

    Returns 404 error if user not found.
    """
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
