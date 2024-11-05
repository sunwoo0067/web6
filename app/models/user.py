from sqlalchemy import Boolean, Column, Integer, String
<<<<<<< HEAD
from app.db.base import Base
=======
from sqlalchemy.orm import relationship
from app.db.base_class import Base
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
<<<<<<< HEAD
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
=======
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    profile = relationship("Profile", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="user")
    files = relationship("File", back_populates="user")
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
