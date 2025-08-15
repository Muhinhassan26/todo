from fastapi import APIRouter,Request,Depends,Form
from typing import Annotated,Any
from src.modules.todos.services import TodoService
from src.core.html_renderer import HtmlRenderer
from fastapi.responses import HTMLResponse,RedirectResponse
from src.core.auth import require_login
from src.modules.todos.schemas import TodoCreate,TodoUpdate
from src.core.schemas.common import QueryParams




router = APIRouter(prefix="/user", tags=["Todos"])
renderer = HtmlRenderer()


@router.get("/todos/", response_class=HTMLResponse)
async def get_todo_list(
    todo_service:Annotated[TodoService,Depends()],
    user_id:Annotated[int,Depends(require_login)],
    request: Request,
    pagination:Annotated[QueryParams,Depends()], 
    search: str|None=None,
    filter:str='all',

) -> Any:
    
    search_fields=["title","description"]

    todos, total_count = await todo_service.get_user_todos_paginated(
        user_id=user_id,
        search_fields=search_fields,
        page=pagination.page,
        page_size=pagination.page_size,
        search=search,
        filter_by=filter,
    )

    has_next=pagination.page * pagination.page_size < total_count

    total_pages = (total_count + pagination.page_size - 1) // pagination.page_size


    return await renderer.render(
        request=request,
        template="todo/list.html",
        data={'user_id':user_id,
            "todos": todos,
            "page": pagination.page,
            "limit": pagination.page_size,
            "has_next":has_next,
            "total_pages": total_pages,
            'search':search,
            'filter':filter,
        },
    )



    
@router.get("/create/", response_class=HTMLResponse)
async def add_todo_form(
    request: Request,
    user_id: Annotated[int, Depends(require_login)]
):
    return await renderer.render(
        request=request,
        template="todo/todo.html",
        data={
            'user_id':user_id
        }

    )


@router.post("/create/", response_class=RedirectResponse)
async def create_todo(
    request: Request,
    data:Annotated[TodoCreate,Form()],
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
     

    await todo_service.create_todo(user_id, data)
    return RedirectResponse(url="/todos/user/todos/", status_code=303) 


@router.post("/update/{todo_id}", response_class=RedirectResponse)
async def update_todo(
    todo_id: int,
    request: Request,
    data:Annotated[TodoUpdate,Form()],
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
    update_data = TodoUpdate(
        **data.model_dump()
    )
    await todo_service.update_todo(todo_id, user_id, update_data)
    return RedirectResponse(url="/todos/user/todos/", status_code=303)



@router.post("/delete/{todo_id}", response_class=RedirectResponse)
async def delete_todo(
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
    await todo_service.delete_todo(user_id=user_id, todo_id=todo_id)
    return RedirectResponse(url="/todos/user/todos/", status_code=303)