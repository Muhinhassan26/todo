from typing import  Any, Annotated
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from src.core.html_renderer import HtmlRenderer
from src.modules.auth.schemas import LoginData
from src.modules.auth.services import UserAuthService


router = APIRouter(prefix="/user")



@router.get("/signup/", response_class=HTMLResponse)
async def get_signup_page(request: Request) -> Any:
    renderer = HtmlRenderer()
    return  await renderer.render(
        request=request,
        template="auth/signup.html",
    )


@router.post("/signup", response_class=HTMLResponse)
async def process_signup(
    data: Annotated[LoginData, Form()],
    user_auth_service: Annotated[UserAuthService, Depends(UserAuthService)]
) -> Any:
    await user_auth_service.process_login(data=data)
