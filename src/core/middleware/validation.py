from fastapi import Request
from fastapi.exceptions import RequestValidationError
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import field_error_format


async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> Exception:
    details = exc.errors()
    print(details)
    # errors = field_error_format(details)  # type: ignore
    # return ValidationException(errors=errors)
