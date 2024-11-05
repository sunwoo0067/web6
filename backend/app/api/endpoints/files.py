import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.crud import file as file_crud
from app.schemas.file import File, FileCreate
from app.core.security import get_current_user_from_token
from app.db.session import get_db

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=File, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Get file size
    file_size = len(content)

    # Create file record in database
    file_create = FileCreate(
        filename=file.filename,
        content_type=file.content_type,
        file_path=file_path,
        user_id=current_user_id,
        file_size=file_size
    )
    db_file = file_crud.create_file(db, file_create)
    return db_file

@router.get("/my-files", response_model=List[File])
def read_user_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    files = file_crud.get_user_files(db, current_user_id, skip=skip, limit=limit)
    return files

@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file = file_crud.get_file(db, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(
        file.file_path,
        media_type=file.content_type,
        filename=file.filename
    )

@router.get("/{file_id}", response_model=File)
def read_file(file_id: int, db: Session = Depends(get_db)):
    file = file_crud.get_file(db, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.delete("/{file_id}", response_model=File)
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_from_token)
):
    file = file_crud.get_file(db, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if file.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete file from disk
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    return file_crud.delete_file(db, file_id)
