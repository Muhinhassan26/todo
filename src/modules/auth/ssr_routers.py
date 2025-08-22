from fastapi import APIRouter
from src.modules.auth.controllers import user_router

api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix="/auth",
    tags=["User Auth"],
)
