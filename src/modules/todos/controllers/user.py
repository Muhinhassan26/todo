from fastapi import APIRouter, Depends, status, Query
from typing import Annotated, List, Optional
from src.modules.todos.services import TodoService
from src.modules.todos.schemas import TodoCreate, TodoUpdate, TodoRead
from src.core.auth import require_login


router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("/", response_model=List[TodoRead])
async def get_user_todos(
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> List[TodoRead]:
    return await todo_service.get_user_todos(user_id)


@router.get("/paginated", response_model=List[TodoRead])
async def get_user_todos_paginated(
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
    filter: str = Query("all", regex="^(all|completed|not_completed)$"),
):
    skip = (page - 1) * limit
    todos, has_next = await todo_service.get_user_todos_paginated(
        user_id=user_id, skip=skip, limit=limit, search=search, filter=filter
    )
    return todos


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
):
    return await todo_service.get_todo(todo_id, user_id)


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    data: TodoCreate,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
):
    return await todo_service.create_todo(user_id, data)


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    data: TodoUpdate,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
):
    return await todo_service.update_todo(todo_id, user_id, data)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
):
    await todo_service.delete_todo(todo_id, user_id)