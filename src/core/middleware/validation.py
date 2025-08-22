from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.core.error.codes import REGISTRATION_FAILED
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import field_error_format


async def validation_exception_handler(
    _: Request,
    exc: Exception,  # <- change here
) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        details = exc.errors()
        errors = field_error_format(details, is_pydantic_validation_error=True)  # type: ignore
        ve = ValidationException(errors=errors, error_code=REGISTRATION_FAILED)

        return JSONResponse(
            status_code=ve.code,
            content={
                "error_code": ve.error_code,
                "message": ve.message,
                "errors": ve.errors,
            },
        )
    # fallback for unexpected exceptions
    raise exc
