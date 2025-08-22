from typing import Annotated

from fastapi import APIRouter, Depends, status
from src.core.logger import logger
from src.modules.auth.schemas import TokenResponse, UserLoginSchema, UserRegisterSchema
from src.modules.auth.services import UserAuthService

router = APIRouter(prefix="/user")


@router.post("/signup/", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def process_signup(
    data: UserRegisterSchema,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
) -> TokenResponse:
    return await user_auth_service.register(user_data=data)


@router.post("/login/", response_model=TokenResponse)
async def process_login(
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    form_data: UserLoginSchema,
) -> TokenResponse:
    tokens = await user_auth_service.login_user(form_data)
    logger.info(f"Login successful for user_id={tokens.user_id}")
    return tokens


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user() -> dict:
    return {"message": "Logout successful. Please delete your tokens on the client side."}
