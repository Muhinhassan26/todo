from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.core.logger import logger
from src.core.security.jwt_handler import JWTHandler
from src.modules.auth.schemas import AccessTokenPayload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)

    async def verify_jwt(self, token: str) -> tuple[bool, AccessTokenPayload | None]:
        try:
            payload = AccessTokenPayload(**JWTHandler.decode(token=token))
            return True, payload
        except (HTTPException, Exception) as err:  # pylint: disable=broad-exception-caught
            logger.error("JWt invalid %s", err)
            return False, None

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        assert credentials is not None

        jwt_token = credentials.credentials
        is_verified_jwt, decoded_data = await self.verify_jwt(token=jwt_token)
        if not is_verified_jwt or not decoded_data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        request.state.user = decoded_data.model_dump(exclude={"exp"})
        return credentials
