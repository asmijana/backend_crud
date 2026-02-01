from __future__ import annotations
from fastapi import Depends, Header, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import User

def get_current_user(x_user_id : int = Header(alias="X-User-ID"), session : Session = Depends(get_session)) -> User:
    """
    Very simple 'auth' dependency:
    - Reads X-User-Id from the request headers.
    - Loads that user from the DB.
    """
    statement = select(User).where(User.id == x_user_id)
    user = session.exec(statement).first()
    if user is None:
        raise HTTPException(status_code = 401, detail = "Invalid X-User-ID header")
    return user