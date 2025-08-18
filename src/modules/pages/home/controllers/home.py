from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from src.core.html_renderer import HtmlRenderer

router = APIRouter()
renderer = HtmlRenderer()


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request) -> Any:
    return await renderer.render(request=request, template="pages/index.html")
