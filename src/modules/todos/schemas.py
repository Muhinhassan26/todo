from datetime import datetime

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    priority: int = Field(ge=1, le=5)
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    priority: int | None = Field(ge=1, le=5, default=None)
    completed: bool | None = False


class TodoRead(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    completed: bool
    created_at: datetime
    updated_at: datetime
