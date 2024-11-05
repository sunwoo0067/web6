from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate

def get_profile(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()

def create_profile(db: Session, profile: ProfileCreate, user_id: int):
    db_profile = Profile(**profile.model_dump(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile: ProfileUpdate, user_id: int):
    db_profile = get_profile(db, user_id)
    if not db_profile:
        return None
    
    for key, value in profile.model_dump(exclude_unset=True).items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, user_id: int):
    db_profile = get_profile(db, user_id)
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return db_profile
