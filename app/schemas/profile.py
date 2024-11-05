from pydantic import BaseModel, ConfigDict

class ProfileBase(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int
