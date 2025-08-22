from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, status
from src.core.depedencies.query_params import CommonQueryParam
from src.core.schemas.common import PaginatedResponse, QueryParams, ResponseMessage
from src.modules.todos.schemas import TodoCreate, TodoResponse, TodoUpdate
from src.modules.todos.services import TodoService

router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[TodoResponse])
async def get_user_todos(
    request: Request,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    user_id = request.state.user["user_id"]
    return await todo_service.get_user_todos(user_id=int(user_id))


@router.get("/paginated/", response_model=PaginatedResponse[TodoResponse])
async def get_todo_list(
    request: Request,
    todo_service: Annotated[TodoService, Depends()],
    query_params: QueryParams = Depends(CommonQueryParam(filter_fields=["completed", "search"])),
) -> Any:
    user_id = int(request.state.user["user_id"])
    return await todo_service.get_user_todos_paginated(
        user_id=user_id,
        query_params=query_params,
    )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_(
    request: Request,
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    user_id = int(request.state.user["user_id"])
    return await todo_service.get_todo(todo_id=todo_id, user_id=user_id)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    request: Request,
    data: TodoCreate,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    user_id = int(request.state.user["user_id"])
    return await todo_service.create_todo(user_id=user_id, data=data)


@router.put("/{todo_id}", response_model=ResponseMessage)
async def update_todo(
    request: Request,
    todo_id: int,
    data: TodoUpdate,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    user_id = int(request.state.user["user_id"])
    await todo_service.update_todo(todo_id=todo_id, user_id=user_id, data=data)
    return ResponseMessage(message="Todo updated succesfully")


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK, response_model=ResponseMessage)
async def delete_todo(
    request: Request,
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    user_id = int(request.state.user["user_id"])
    await todo_service.delete_todo(todo_id=todo_id, user_id=user_id)
    return ResponseMessage(message=f"The todo with id {todo_id} of user id {user_id} deleted!")
