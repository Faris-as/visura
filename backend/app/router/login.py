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
from ..security import verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=schemas.LoginResponse)
async def register(user: schemas.LoginCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email Aldready Registered")
    new_user = crud.create_user(db, user)
    return schemas.LoginResponse.model_validate(new_user)

@router.post("/login", response_model=schemas.TokenResponse)
async def login(user: schemas.LoginRequest, db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not db_user.is_active:
        db_user.is_active = True
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    token_data = {
        "sub": str(db_user.id), 
        "role": db_user.role.value if hasattr(db_user.role, "value") else str(db_user.role)
    }
    access_token = create_access_token(token_data)
    return schemas.TokenResponse(
        access_token = access_token, 
        token_type = "bearer", 
        user = schemas.LoginResponse.model_validate(db_user)
    )