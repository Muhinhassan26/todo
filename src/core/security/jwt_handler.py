from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from fastapi import HTTPException, status
from src.core.config import settings
from src.core.logger import logger
from src.modules.auth.schemas import AccessTokenPayload, RefreshTokenPayload


class JWTHandler:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_expire_minutes = settings.ACCESS_TOKEN_EXPIRY_MINUTES
    refresh_expire_minutes = settings.REFRESH_TOKEN_EXPIRY_MINUTES

    @staticmethod
    def encode(
        token_type: Literal["access", "refresh"],
        payload: AccessTokenPayload | RefreshTokenPayload,
    ) -> tuple[str, datetime]:
        expire_minutes = (
            JWTHandler.access_expire_minutes
            if token_type == "access"
            else JWTHandler.refresh_expire_minutes
        )

        expire = datetime.now(UTC) + timedelta(minutes=expire_minutes)
        payload.exp = expire
        return str(
            jwt.encode(
                payload.model_dump(),
                JWTHandler.secret_key,
                algorithm=JWTHandler.algorithm,
            )
        ), expire

    @staticmethod
    def decode(token: str) -> Any:
        try:
            return jwt.decode(token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm])
        except jwt.PyJWTError as exception:
            logger.error("JWT invalid %s", exception)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token. Please log in again."
            ) from exception

    @staticmethod
    def decode_expired(token: str) -> Any:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except jwt.PyJWTError as exception:
            logger.error("JWT decoding failed (even without expiry check): %s", exception)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token."
            ) from exception
