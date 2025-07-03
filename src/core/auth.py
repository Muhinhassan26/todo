from fastapi import Request, Depends, HTTPException, status
from typing import Annotated
from src.core.security import JWTHandler
from src.core.logger import logger
from src.core.error.exceptions import UnauthorizedException
from src.core.flash import flash_message


def get_current_user_id(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        logger.warning("Missing access token in cookies")
        raise UnauthorizedException("Access token is missing. Please log in again.")

    try:
        payload = JWTHandler.decode(token)
        user_id = payload.get("user_id")
        if not user_id:
             raise UnauthorizedException("Invalid token: Missing user ID.")
        return int(user_id)

    except Exception as e:
        logger.error(f"Access token decoding failed: {e}")
        raise UnauthorizedException("Your session has expired. Please log in again.")


def require_login(request: Request) -> int:
    try:
        user_id = get_current_user_id(request)
        return user_id

    except UnauthorizedException as e:
        
        flash_message(request, msg=getattr(e, "message", "Unauthorized"), category="danger")

        
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"HX-Redirect": "/auth/user/login/"}
        )