from typing import  Any, Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from src.core.html_renderer import HtmlRenderer
from src.modules.auth.schemas import UserRegisterSchema,UserLoginSchema
from src.modules.auth.services import UserAuthService
from src.core.flash import get_flash_messages
from pydantic import ValidationError
from src.core.logger import logger
from src.core.error.exceptions import ValidationException




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
    renderer = HtmlRenderer()
    try:
        await user_auth_service.register(user_data=data)
        return await renderer.render(
            request=request,
            template="todo/todo.html",
            messages=[{"category": "success", "message": "Signup successful!"}],
            data=data,
        )
    except ValidationError as e:
        error_messages = [
            {"category": "danger", "message": err["msg"]} for err in e.errors()
        ]
        return await renderer.render(
            request=request,
            template="auth/signup.html",
            messages=error_messages,
            data=data,
        )
    except Exception as e:
        return await renderer.render(
            request=request,
            template="auth/signup.html",
            messages=[{"category": "danger", "message": str(e)}],
            data=data,
        )
    

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
    renderer = HtmlRenderer()
    try:
        tokens = await user_auth_service.login_user(data=data)

        response = await renderer.render(
            request=request,
            template="todo/todo.html",
            messages=[{"category": "success", "message": "Login successful!"}]
        )

       
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
        )

        
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
        )
        logger.info(f"Login successful for user_id={tokens.user_id}")
        return response
    


    except ValidationException as ve:
        logger.warning(f"Login failed: {ve.message} - {ve.errors}")

        error_messages = [
            {"category": "danger", "message": msg}
            for msg in ve.errors.values()
        ]

        return await renderer.render(
            request=request,
            template="auth/login.html",
            messages=error_messages,
            data=data,
        )