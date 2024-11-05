from sqlalchemy.orm import Session
from app.models.file import File
from app.schemas.file import FileCreate

def create_file(db: Session, file: FileCreate):
    db_file = File(**file.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()

def get_user_files(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(File).filter(File.user_id == user_id).offset(skip).limit(limit).all()

def delete_file(db: Session, file_id: int):
    db_file = get_file(db, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file
