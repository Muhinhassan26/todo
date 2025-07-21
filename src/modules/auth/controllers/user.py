from typing import  Any, Annotated
from fastapi import APIRouter, Depends, Request, Form,status
from fastapi.responses import HTMLResponse, RedirectResponse
from src.core.html_renderer import HtmlRenderer
from src.modules.auth.schemas import UserRegisterSchema,UserLoginSchema,TokenResponse
from src.modules.auth.services import UserAuthService
from src.core.flash import get_flash_messages
from pydantic import ValidationError
from src.core.logger import logger
from src.core.error.exceptions import ValidationException
from src.core.flash import flash_message



router = APIRouter(prefix="/user")



# @router.get("/signup/", response_class=HTMLResponse)
# async def get_signup_page(request: Request) -> Any:
#     renderer = HtmlRenderer()
#     messages = get_flash_messages(request)
#     return  await renderer.render(
#         request=request,
#         template="auth/signup.html",
#         messages=messages,
#     )


@router.post("/signup/", response_model=UserRegisterSchema,status_code=status.HTTP_201_CREATED)
async def process_signup(
    data: UserRegisterSchema,
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
) -> dict:
    
    await user_auth_service.register(user_data=data)
    return {"message": "User registered successfully"}

    

# @router.get("/login/", response_class=HTMLResponse)
# async def get_login_page(request: Request) -> Any:
#     renderer = HtmlRenderer()
#     messages = get_flash_messages(request)
  
#     return await renderer.render(
#         request=request,
#         template="auth/login.html",
#         messages=messages
#     )

@router.post('/login/',response_model=TokenResponse)
async def process_login(
 
    data:UserLoginSchema,
    user_auth_service:Annotated[UserAuthService,Depends(UserAuthService)]
 
) -> TokenResponse:

    tokens = await user_auth_service.login_user(login_data=data)
        
    logger.info(f"Login successful for user_id={tokens.user_id}")
    return tokens
    

@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user() -> dict:
    return {"message": "Logout successful. Please delete your tokens on the client side."}
