from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(100), nullable=False)
    email=Column(String(150), unique=True, index=True, nullable=False)
    phone=Column(String(15),nullable=True,index=True)
    password_hash=Column(String(255),nullable=False)
    role=Column(String(20), default="user", nullable=False) #"user" or "admin"
    latitude=Column(Float, nullable=True,index=True)
    longitude=Column(Float, nullable=True, index=True)
    created_at=Column(DateTime, server_default=func.now())
    updated_at=Column(DateTime,onupdate=func.now())
    trees=relationship("Tree", back_populates="uploader")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"

