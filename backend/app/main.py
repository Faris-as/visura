"""
Main app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db
from .router import crud, login

app = FastAPI(
    title="Login Section API",
    description="Login System",
    version="1.0.10"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(login.router)

@app.get("/", tags=["root"])
def root():
    return {
        "message": "Welcome",
        "docs": "/docs",
        "endpoints":
            {
                "POST login": "for logging in",
                "POST register": "for registering"
            }
    }