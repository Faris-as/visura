"""
Login Opreation
- Login
- Register
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from . import crud
from ..database import get_db
from ..security import verify_password

router = APIRouter()

@router.post("/register", response_model=schemas.LoginResponse)
def register(user: schemas.LoginCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email Aldready Registered")
    new_user = crud.create_user(db, user)
    return new_user

@router.post("/login", response_model=schemas.LoginResponse)
def login(user: schemas.LoginRequest, db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db.user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "message": "Login Successful"
    }