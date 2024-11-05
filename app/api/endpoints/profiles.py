from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import profile as profile_crud
from app.db.session import get_db
from app.schemas.profile import Profile, ProfileCreate, ProfileUpdate

router = APIRouter()

@router.get("/{user_id}", response_model=Profile)
def read_profile(user_id: int, db: Session = Depends(get_db)):
    db_profile = profile_crud.get_profile(db, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.post("/{user_id}", response_model=Profile)
def create_profile(
    user_id: int,
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    db_profile = profile_crud.get_profile(db, user_id=user_id)
    if db_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return profile_crud.create_profile(db=db, profile=profile, user_id=user_id)

@router.put("/{user_id}", response_model=Profile)
def update_profile(
    user_id: int,
    profile: ProfileUpdate,
    db: Session = Depends(get_db)
):
    db_profile = profile_crud.update_profile(db=db, profile=profile, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    db_profile = profile_crud.delete_profile(db=db, user_id=user_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"status": "success"}
