"""
CRUD Operations
"""

from sqlalchemy.orm import Session
from .. import models, schemas
from .. security import hash_password

def create_user(db:Session, user:schemas.LoginCreate):
    hashed_password = hash_password(user.password)
    db_user = models.Login(
        username = user.username,
        email = user.email,
        password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db:Session, email: str):
    return db.query(models.Login).filter(models.Login.email == email).first()