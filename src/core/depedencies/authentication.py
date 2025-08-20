# from fastapi import Request
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from src.core.error.codes import FORBIDDEN_ERROR
# from src.core.error.exceptions import JWTError
# from src.core.error.format_error import ERROR_MAPPER
# from src.core.logger import logger
# from src.core.security.jwt_handler import JWTHandler
# from src.modules.auth.schemas import AccessTokenPayload


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True) -> None:
#         super().__init__(auto_error=auto_error)

#     async def verify_jwt(self, token: str) -> tuple[bool, AccessTokenPayload | None]:
#         try:
#             payload = AccessTokenPayload(**JWTHandler.decode(token=token))
#             return True, payload
#         except (JWTError, Exception) as err:  # pylint: disable=broad-exception-caught
#             logger.error("JWK invalid %s", err)
#             return False, None

#     async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
#         credentials = await super().__call__(request)
#         assert credentials is not None

#         jwt_token = credentials.credentials
#         is_verified_jwt, decoded_data = await self.verify_jwt(token=jwt_token)
#         if not is_verified_jwt or not decoded_data:
#             raise JWTError(errors=ERROR_MAPPER[FORBIDDEN_ERROR])

#         request.state.user = decoded_data.model_dump(exclude={"exp"})
#         return credentials


from fastapi import HTTPException, Request, status
from src.core.error.exceptions import UnauthorizedException
from src.core.flash import flash_message
from src.core.security import JWTHandler


def get_current_user_id(request: Request) -> int | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = JWTHandler.decode(token)
        user_id = payload.get("user_id")
        if not user_id:
            return None
        return int(user_id)
    except Exception:
        return None


async def require_login(request: Request) -> int:
    try:
        current_user = get_current_user_id(request)
        if not current_user:
            flash_message(request, msg="Unauthorized", category="danger")
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                headers={"Location": "/auth/user/login/"},
            ) from None
        return current_user
    except UnauthorizedException as e:
        flash_message(request, msg=getattr(e, "message", "Unauthorized"), category="danger")
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/auth/user/login/"},
        ) from None
