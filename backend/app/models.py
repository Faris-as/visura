"""
Database Models (SQLAlchemy)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
from .database import Base
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    developer = "developer"

class Login(Base):
    """
    Fields to add:

    id
    username
    email 
    password (hashed): security important
    created_at
    updated_at
    admin/ role : so we can know whether they are developer or not
    """
    __tablename__ = "login"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(50), unique= True, nullable=False, index=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default = False)
    role = Column(SAEnum(RoleEnum, name="roleenum", native_enum=True), nullable=False, server_default=RoleEnum.user.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<Login(username={self.username}, email={self.email}, admin={self.is_admin})>"