from __future__ import annotations
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import User
from app.schemas import UserCreate, UserRead
from app.db import get_session

router = APIRouter(prefix="/users", tags = ["users"])

@router.post("/", response_model=UserRead)
def create_user(usr : UserCreate, session : Session = Depends(get_session)):
    statement  = select(User).where(User.email == usr.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_usr = User(email = usr.email, full_name = usr.full_name)
    session.add(db_usr)
    session.commit()
    session.refresh(db_usr)
    return db_usr

@router.get("/", response_model = List[UserRead])
def list_users(session : Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.get("/{usr_id}", response_model = UserRead)
def get_user(usr_id : int, session : Session = Depends(get_session)):
    statement = select(User).where(User.id == usr_id)
    usr = session.exec(statement).first()
    if usr is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return usr

@router.delete("/{usr_id}")
def delete_usr(usr_id : int, session : Session = Depends(get_session)):
    statement = select(User).where(User.id == usr_id)
    usr = session.exec(statement).first()
    if usr is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    session.delete(usr)
    session.commit()
    return {"detail" : "User deleted"}