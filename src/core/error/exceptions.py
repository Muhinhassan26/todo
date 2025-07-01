
from fastapi import status

class CustomException(Exception):
    code = status.HTTP_502_BAD_GATEWAY
    message = "Bad Gateway"


    def __init__(self, message: str | None = None, errors: dict[str, str] | None = None) -> None:
        self.message = message or self.message
        self.errors = errors or {}
        
        
    def __str__(self) -> str:
        return f"{self.message} -> {self.errors if self.errors else ''}"

    


class DatabaseException(CustomException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Database Error"



class ValidationException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    message = "Validation failed"


class NotFoundException(CustomException):
    code = status.HTTP_404_NOT_FOUND
    message = "Not found"


class JWTError(CustomException):
    code = status.HTTP_403_FORBIDDEN
    message = "Not authenticated"

class UnauthorizedException(Exception):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Not authenticated"