from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel

#Users

class UserCreate(SQLModel):
    email : str
    full_name : str

class UserRead(SQLModel):
    id : int
    email : str
    full_name : str

#Experiments

class ExperimentCreate(SQLModel):
    name : str
    description : str
    
    
class ExperimentRead(SQLModel):
    id : int
    name : str
    description : str
    owner_id : int

class ExperimentUpdate(SQLModel):
    name: Optional[str] = None
    description : Optional[str] = None
