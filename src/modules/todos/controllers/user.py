from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from src.core.depedencies import CommonQueryParam, require_login
from src.core.html_renderer import HtmlRenderer
from src.core.schemas.common import QueryParams
from src.modules.todos.schemas import TodoCreate, TodoUpdate
from src.modules.todos.services import TodoService

router = APIRouter(prefix="/user", tags=["Todos"])
renderer = HtmlRenderer()


@router.get("/todos/", response_class=HTMLResponse)
async def get_todo_list(
    request: Request,
    user_id: Annotated[int, Depends(require_login)],
    todo_service: Annotated[TodoService, Depends()],
    query_params: QueryParams = Depends(CommonQueryParam(filter_fields=["completed", "search"])),
) -> Any:
    response = await todo_service.get_user_todos_paginated(
        user_id=user_id,
        query_params=query_params,
    )

    return await renderer.render(
        request=request,
        template="todo/list.html",
        data={
            "user_id": user_id,
            "todos": response.data,
            "page": response.meta.current_page,
            "limit": response.meta.page_size,
            "has_next": response.meta.last_page > response.meta.current_page,
            "total_pages": response.meta.last_page,
        },
    )


@router.get("/create/", response_class=HTMLResponse)
async def add_todo_form(
    request: Request,
    user_id: Annotated[int, Depends(require_login)],
) -> Any:  # noqa: ARG001
    return await renderer.render(
        request=request, template="todo/todo.html", data={"user_id": user_id}
    )


@router.post("/create/", response_class=RedirectResponse)
async def create_todo(
    request: Request,  # noqa: ARG001
    user_id: Annotated[int, Depends(require_login)],
    data: Annotated[TodoCreate, Form()],
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    await todo_service.create_todo(user_id, data)
    return RedirectResponse(url="/todos/user/todos/", status_code=303)


@router.post("/update/{todo_id}", response_class=RedirectResponse)
async def update_todo(
    request: Request,  # noqa: ARG001
    todo_id: int,
    user_id: Annotated[int, Depends(require_login)],
    data: Annotated[TodoUpdate, Form()],
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    await todo_service.update_todo(todo_id=todo_id, user_id=user_id, data=data)
    return RedirectResponse(url="/todos/user/todos/", status_code=303)


@router.post("/delete/{todo_id}", response_class=RedirectResponse)
async def delete_todo(
    request: Request,  # noqa: ARG001
    user_id: Annotated[int, Depends(require_login)],
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
) -> Any:
    await todo_service.delete_todo(user_id=user_id, todo_id=todo_id)
    return RedirectResponse(url="/todos/user/todos/", status_code=303)
