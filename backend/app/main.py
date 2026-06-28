from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.db.database import engine, get_db
from app.db import models
from app.routers import users, auth, questionnaire, analytics

import time

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/debug/db")
def debug_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()

        url = str(db.bind.url)

        tables = db.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        )).fetchall()

        return {
            "connected_to": url,
            "tables": [t[0] for t in tables]
        }

    except Exception as e:
        return {"error": str(e)}
    
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(questionnaire.router)
app.include_router(analytics.router)
