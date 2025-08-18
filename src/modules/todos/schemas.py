from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    priority: int = Field(ge=1, le=5)
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int
