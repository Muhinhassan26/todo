from fastapi import APIRouter,Request,Depends,Form
from typing import Annotated,Any
from src.modules.todos.services import TodoService
from src.core.html_renderer import HtmlRenderer
from fastapi.responses import HTMLResponse,RedirectResponse
from src.core.auth import require_login
from src.modules.todos.schemas import TodoCreate,TodoUpdate
from src.core.error.exceptions import UnauthorizedException
from src.core.flash import flash_message



router = APIRouter(prefix="/todos", tags=["Todos"])
renderer = HtmlRenderer()


@router.get("/", response_class=HTMLResponse)
async def get_todo_list(
    request: Request,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
    
    todos = await todo_service.get_user_todos(user_id)

    return await renderer.render(
            request=request,
            template="todo/todo.html",
            data={"todos": todos}
        )
    



@router.post("/create", response_class=RedirectResponse)
async def create_todo(
    request: Request,
    data:Annotated[TodoCreate,Form()],
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
     
    todo_data = TodoCreate(
            **data.model_dump()
        )
    await todo_service.create_todo(user_id, todo_data)
    return RedirectResponse(url="/todos", status_code=303) 


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
    return RedirectResponse(url="/todos", status_code=303)



@router.post("/delete/{todo_id}", response_class=RedirectResponse)
async def delete_todo(
    todo_id: int,
    todo_service: Annotated[TodoService, Depends()],
    user_id: Annotated[int, Depends(require_login)],
) -> Any:
    await todo_service.delete_todo(todo_id, user_id)
    return RedirectResponse(url="/todos", status_code=303)