from collections.abc import Callable
from typing import Any

from fastapi.responses import RedirectResponse
from src.core.error.codes import INVALID_CRED
from src.core.error.exceptions import CustomException
from src.core.error.format_error import ERROR_MAPPER
from src.core.flash import flash_message
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        try:
            return await call_next(request)
        except CustomException as exc:
            msg = ERROR_MAPPER.get(getattr(exc, "error_code", None), exc.message)
            flash_message(request=request, msg=msg, errors=exc.errors, category="error")

            if getattr(exc, "error_code", None) == INVALID_CRED:
                return RedirectResponse(url="/auth/user/login/", status_code=302)
            return RedirectResponse(url=request.url.path, status_code=302)
