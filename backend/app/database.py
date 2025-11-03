"""
Database Connection Setup
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .env import DATABASE_URL

# Database Engine
engine = create_engine(DATABASE_URL, echo=True)

# Database Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base

def get_db():
    """
    Generator function 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()