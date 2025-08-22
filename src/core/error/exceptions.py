from typing import Any

from fastapi import status
from src.core.error.codes import (
    EMAIL_ALREADY_EXISTS,
    FORBIDDEN_ERROR,
    INTERNAL_ERROR,
    INVALID_CRED,
    INVALID_USER,
    NO_DATA,
    REGISTRATION_FAILED,
    UNAUTHORIZED_ERROR,
    USER_EXISTS,
)
from src.core.error.format_error import ERROR_MAPPER


class CustomException(Exception):
    code = status.HTTP_502_BAD_GATEWAY
    message: str = ERROR_MAPPER.get(INTERNAL_ERROR) or "Bad Gateway"

    def __init__(
        self,
        message: str | None = None,
        errors: str | dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        self.error_code: str = str(error_code or getattr(self, "error_code", INTERNAL_ERROR))
        self.message: str = message or ERROR_MAPPER.get(self.error_code) or "Unknown error"
        self.errors = errors or ""

    def __str__(self) -> str:
        return f"{self.message} -> {self.errors if self.errors else ''}"


class ValidationException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = REGISTRATION_FAILED
    message: str = ERROR_MAPPER.get(REGISTRATION_FAILED) or "Validation failed"


class NotFoundException(CustomException):
    code = status.HTTP_404_NOT_FOUND
    error_code = NO_DATA
    message: str = ERROR_MAPPER.get(NO_DATA) or "Not found"


class UnauthorizedException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = UNAUTHORIZED_ERROR
    message: str = ERROR_MAPPER.get(UNAUTHORIZED_ERROR) or "Login Required"


class ForbiddenException(CustomException):
    code = status.HTTP_403_FORBIDDEN
    error_code = FORBIDDEN_ERROR
    message: str = ERROR_MAPPER.get(FORBIDDEN_ERROR) or "Forbidden"


class InvalidCredentialsException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = INVALID_CRED
    message: str = ERROR_MAPPER.get(INVALID_CRED) or "Invalid credentials"


class UserExistsException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = USER_EXISTS
    message: str = ERROR_MAPPER.get(USER_EXISTS) or "User already exists"


class EmailAlreadyExistsException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = EMAIL_ALREADY_EXISTS
    message: str = ERROR_MAPPER.get(EMAIL_ALREADY_EXISTS) or "Email already in use"


class InvalidUserException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = INVALID_USER
    message: str = ERROR_MAPPER.get(INVALID_USER) or "Invalid user"


class InternalServerException(CustomException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = INTERNAL_ERROR
    message: str = ERROR_MAPPER.get(INTERNAL_ERROR) or "Internal Server Error"
