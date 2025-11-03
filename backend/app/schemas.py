"""
Pydantic Schema for validation 
"""
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class LoginBase(BaseModel):
    # Base
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class LoginCreate(LoginBase):
    """Registration of Login"""
    password: str = Field(..., min_length=8, max_length=200)
        
class LoginResponse(BaseModel):
    """Login Response"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True # Take directly from ORM
        
        
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

