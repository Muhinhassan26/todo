from typing import  Any, Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from src.core.html_renderer import HtmlRenderer
from src.modules.auth.schemas import LoginData
from src.modules.auth.services import UserAuthService
from src.core.flash import get_flash_messages

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
    data: Annotated[LoginData, Form()],
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)]
) -> Any:
    await user_auth_service.process_login(data=data)
