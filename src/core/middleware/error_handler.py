from collections.abc import Callable
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError

class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        try:
            print('-----------------------')
            return await call_next(request)
        except RequestValidationError as exc:
            print(f"Validation error: {exc.errors()}")