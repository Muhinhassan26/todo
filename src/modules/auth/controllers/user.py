from typing import  Annotated
from fastapi import APIRouter, Depends, status
from src.modules.auth.schemas import UserRegisterSchema,UserLoginSchema,TokenResponse
from src.modules.auth.services import UserAuthService
from src.core.logger import logger
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user")


@router.post("/signup/", response_model=UserRegisterSchema,status_code=status.HTTP_201_CREATED)
async def process_signup(
    data: UserRegisterSchema,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
) -> dict:
    
    create_user=await user_auth_service.register(user_data=data)
    return create_user


@router.post('/login/',response_model=TokenResponse)
async def process_login(
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
    form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
     tokens = await user_auth_service.login_user(form_data)
     logger.info(f"Login successful for user_id={tokens.user_id}")
     return tokens
    

@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user() -> dict:
    return {"message": "Logout successful. Please delete your tokens on the client side."}
