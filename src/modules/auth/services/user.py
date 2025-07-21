from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.modules.users.repository import UserRepository
from src.modules.auth.schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    TokenResponse,
    AccessTokenPayload,
    RefreshTokenPayload,
)
from src.core.logger import logger
from src.core.security import password_handler, JWTHandler
from src.modules.users.models import User


class UserAuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository
        self.logger = logger

    async def register(self, user_data: UserRegisterSchema) -> TokenResponse:
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            self.logger.warning(f"Registration failed: Email already registered - {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )

        hashed_password = password_handler.hash(user_data.password)

        user = User(
            name=user_data.name,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        created_user = await self.user_repository.create(user)
        self.logger.info(f"User registered successfully: user_id={created_user.id}, email={created_user.email}")

        tokens = self.generate_token(user_id=str(created_user.id))
        return tokens

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
                access_token_expire=access_expire
            )

        except Exception as e:
            logger.error(f"Failed to generate token for user_id={user_id} — {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed."
            )

    async def login_user(self, login_data: UserLoginSchema) -> TokenResponse:
        user = await self.user_repository.get_by_email(login_data.email)

        if not user:
            self.logger.warning(f"Login failed: Email not found - {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials: Email not found."
            )

        if not password_handler.verify_password(login_data.password, user.hashed_password):
            self.logger.warning(f"Login failed: Incorrect password for email - {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials: Incorrect password."
            )

        self.logger.info(f"User logged in successfully: user_id={user.id}, email={user.email}")
        tokens = self.generate_token(user_id=str(user.id))
        return tokens
