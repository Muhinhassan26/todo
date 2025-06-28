from collections.abc import Callable
from typing import Any
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.core.error.exceptions import CustomException
from src.core.flash import flash_message
from starlette.responses import RedirectResponse

class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        try:
            return await call_next(request)
        except CustomException as exc:
            flash_message(request=request, msg=exc.message, errors=exc.errors, category="error")
            return RedirectResponse(url=request.url.path, status_code=302)