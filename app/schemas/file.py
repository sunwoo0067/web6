from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class FileBase(BaseModel):
    filename: str
    content_type: str
    file_path: str
    file_size: int

class FileCreate(FileBase):
    user_id: int

class File(FileBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
