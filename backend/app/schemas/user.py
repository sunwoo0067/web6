from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    username: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
