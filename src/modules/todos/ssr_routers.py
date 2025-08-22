from fastapi import APIRouter, Depends
from src.core.depedencies import JWTBearer
from src.modules.todos.controllers import user_router

api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix="/user",
    tags=["User Todo"],
    dependencies=[Depends(JWTBearer())],
)
