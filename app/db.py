from __future__ import annotations
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./experiments.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from app import models
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session: 
        yield session



