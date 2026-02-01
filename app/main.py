from __future__ import annotations
from fastapi import FastAPI
from app.db import init_db
from app.api import experiments as experiments_api
from app.api import users as users_api


app = FastAPI(title="Experiment API")

@app.on_event("startup")
def get_started():
    init_db()

@app.get("/")
def display_root():
    return {"message": "Welcome to the Experiment API"}

app.include_router(experiments_api.router)
app.include_router(users_api.router)
