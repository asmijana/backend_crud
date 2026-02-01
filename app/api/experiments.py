from __future__ import annotations
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from app.db import get_session
from app.models import Experiment, User
from app.schemas import ExperimentCreate, ExperimentRead, ExperimentUpdate
from app.deps import get_current_user
from sqlmodel import select, Session

router = APIRouter(prefix="/experiments", tags = ["experiments"])

@router.post("/", response_model = ExperimentRead)
def create_experiment(exp: ExperimentCreate, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    db_exp = Experiment(name=exp.name, description=exp.description, owner_id = current_user.id)
    session.add(db_exp)
    session.commit()
    session.refresh(db_exp)
    return db_exp

@router.get("/", response_model=List[ExperimentRead])
def list_exp(session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Experiment).where(Experiment.owner_id == current_user.id)
    all_exp = session.exec(statement).all()
    return all_exp

@router.get("/{exp_id}", response_model=ExperimentRead)
def get_exp(exp_id : int, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Experiment).where(Experiment.id == exp_id)
    exp = session.exec(statement).first()
    if exp is None:
        raise HTTPException(status_code = 404, detail = "Experiment not found")
    if exp.owner_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Not allowed to access this experiment")
    return exp

@router.patch("/{exp_id}", response_model = ExperimentRead)
def update_exp(exp_id : int, update_exp: ExperimentUpdate, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Experiment).where(Experiment.id==exp_id)
    exp = session.exec(statement).first()
    if exp is None:
        raise HTTPException(status_code = 404, detail = "Experiment not found")
    if exp.owner_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Not allowed to access this experiment")
    if update_exp.name is not None:
        exp.name = update_exp.name
    if update_exp.description is not None:
        exp.description = update_exp.description
    session.add(exp)
    session.commit()
    session.refresh(exp)
    return exp

@router.delete("/{exp_id}")
def delete_exp(exp_id : int, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Experiment).where(Experiment.id == exp_id)
    exp = session.exec(statement).first()
    if exp is None:
        raise HTTPException(status_code = 404, detail = "Experiment not found")
    if exp.owner_id != current_user.id:
        raise HTTPException(status_code = 403, detail = "Not allowed to access this experiment")
    session.delete(exp)
    session.commit()
    return {"detail" : "Experiment deleted"}




