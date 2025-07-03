import os
from typing import Any

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.core.flash import get_flash_messages
from src.core.auth import get_current_user_id

class HtmlRenderer:
    def __init__(self):
        templates_directory = os.path.join(os.path.dirname(__file__), "../../templates")
        self.templates = Jinja2Templates(
            directory=templates_directory,
                
        )

    
    async def render(
        self,
        request: Request,
        template: str,
        data: Any | None = None,
        messages: dict[str, Any] | None = None,
        status_code: int = 200,
    ) -> HTMLResponse:
        context: dict[str, Any] = {"request": request}
        if data:
            context["data"] = data.model_dump() if hasattr(data, "model_dump") else data
        else:
            context["data"] = {}
        if messages:
            context["messages"] = messages
        context["messages"] = get_flash_messages(request)

        try:
            context["user_id"] = get_current_user_id(request)
        except Exception:
            context["user_id"] = None


        return await self.render_template(
            template,
            context,
            status_code,
        )
    
    async def render_template(
        self,
        template_name: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
    ) -> HTMLResponse:
        return self.templates.TemplateResponse(template_name, context, status_code=status_code)