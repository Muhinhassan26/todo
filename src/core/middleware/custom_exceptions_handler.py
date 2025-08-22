from fastapi import Request
from fastapi.responses import JSONResponse
from src.core.error.exceptions import CustomException


async def custom_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, CustomException)
    return JSONResponse(
        status_code=exc.code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "errors": exc.errors,
        },
    )
