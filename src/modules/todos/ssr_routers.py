from fastapi import APIRouter
from src.modules.todos.controllers import user_router

api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix="/todos",
    tags=["User Todo"],
)
