from typing import Annotated

from fastapi import Depends
from src.core.error.codes import EMAIL_ALREADY_EXISTS
from src.core.error.exceptions import InvalidCredentialsException, ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.logger import logger
from src.core.security import JWTHandler, password_handler
from src.modules.auth.schemas import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenResponse,
    UserLoginSchema,
    UserRegisterSchema,
)
from src.modules.users.models import User
from src.modules.users.repository import UserRepository


class UserAuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository
        self.logger = logger

    async def register(self, user_data: UserRegisterSchema) -> TokenResponse:
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            self.logger.warning(
                f"Registration failed: Email already registered - {user_data.email}"
            )
            raise ValidationException(errors=ERROR_MAPPER[EMAIL_ALREADY_EXISTS])

        hashed_password = password_handler.hash(user_data.password)

        # Create a User SQLAlchemy instance
        user = User(
            name=user_data.name,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
        )

        created_user = await self.user_repository.create(user)
        self.logger.info(
            f"User registered successfully: user_id={created_user.id}, email={created_user.email}"
        )

        return self.generate_token(user_id=str(created_user.id))

    def generate_token(self, user_id: str) -> TokenResponse:
        access_payload = AccessTokenPayload(user_id=user_id, sub="access")
        refresh_payload = RefreshTokenPayload(user_id=user_id, sub="refresh")

        try:
            access_token, access_expire = JWTHandler.encode("access", access_payload)
            refresh_token, _ = JWTHandler.encode("refresh", refresh_payload)

            logger.info(f"Generated tokens for user_id={user_id}")

            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                user_id=user_id,
                access_token_expire=access_expire,
            )

        except Exception as e:
            logger.error(f"Failed to generate token for user_id={user_id} — {str(e)}")
            raise

    async def login_user(self, login_data: UserLoginSchema) -> TokenResponse:
        user = await self.user_repository.get_by_email(login_data.email)

        if not user:
            self.logger.warning(f"Login failed: Email not found - {login_data.email}")
            raise InvalidCredentialsException()

        if not password_handler.verify_password(login_data.password, user.hashed_password):
            self.logger.warning(f"Login failed: Incorrect password for email - {login_data.email}")
            raise InvalidCredentialsException()

        self.logger.info(f"User logged in successfully: user_id={user.id}, email={user.email}")
        return self.generate_token(user_id=str(user.id))
