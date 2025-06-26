from typing import  Any
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from src.core.html_renderer import HtmlRenderer
from typing import Annotated



router = APIRouter(prefix="/user")



@router.get("/signup/", response_class=HTMLResponse)
async def get_signup_page(request: Request) -> Any:
    renderer = HtmlRenderer()
    return  await renderer.render(
        request=request,
        template="auth/signup.html",
    )


