from fastapi import APIRouter

from src.modules.auth.ssr_routers import api_router as auth_router
from src.modules.todos.ssr_routers import api_router as todo_router
from src.modules.pages.home.controllers import api_router as home_router
 

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(todo_router)
api_router.include_router(home_router)