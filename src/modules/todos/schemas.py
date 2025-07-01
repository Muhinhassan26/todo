from pydantic import BaseModel, Field, conint
from typing import Optional
from datetime import datetime


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5) 
    completed: bool = False



class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[int]=Field(ge=1, le=5,default=None)  
    completed: Optional[bool] = None


class TodoRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    created_at: datetime
    updated_at: datetime