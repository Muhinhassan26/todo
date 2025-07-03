from typing import  Any, Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from src.core.html_renderer import HtmlRenderer
from src.modules.auth.schemas import UserRegisterSchema,UserLoginSchema
from src.modules.auth.services import UserAuthService
from src.core.flash import get_flash_messages
from pydantic import ValidationError
from src.core.logger import logger
from src.core.error.exceptions import ValidationException
from src.core.flash import flash_message



router = APIRouter(prefix="/user")



@router.get("/signup/", response_class=HTMLResponse)
async def get_signup_page(request: Request) -> Any:
    renderer = HtmlRenderer()
    messages = get_flash_messages(request)
    return  await renderer.render(
        request=request,
        template="auth/signup.html",
        messages=messages,
    )


@router.post("/signup/", response_class=HTMLResponse)
async def process_signup(
    request: Request,
    data: Annotated[UserRegisterSchema, Form()],
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)],
) -> Any:
    
    await user_auth_service.register(user_data=data)
    return RedirectResponse(url="/auth/user/login/")

    

@router.get("/login/", response_class=HTMLResponse)
async def get_login_page(request: Request) -> Any:
    renderer = HtmlRenderer()
    messages = get_flash_messages(request)
    return await renderer.render(
        request=request,
        template="auth/login.html",
        messages=messages
    )

@router.post('/login/',response_class=HTMLResponse)
async def process_login(
    request:Request,
    data:Annotated[UserLoginSchema,Form()],
    user_auth_service:Annotated[UserAuthService,Depends(UserAuthService)]
 
) -> Any:

    tokens = await user_auth_service.login_user(login_data=data)
    response = RedirectResponse(url="/todos/user/todos/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
    )
    logger.info(f"Login successful for user_id={tokens.user_id}")
    return response
    
@router.post("/logout/")
async def logout_user(request: Request) -> Any:
    response = RedirectResponse(url="/auth/user/login", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    flash_message(request, msg="Logged out successfully", category="success")
    return response

    