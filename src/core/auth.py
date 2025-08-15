from fastapi import Request, Depends, HTTPException, status
from typing import Annotated
from src.core.security import JWTHandler
from src.core.logger import logger
from src.core.error.exceptions import UnauthorizedException
from src.core.flash import flash_message

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
        user_id = get_current_user_id(request)
        return user_id
    except UnauthorizedException as e:
        flash_message(request, msg=getattr(e, "message", "Unauthorized"), category="danger")
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/auth/user/login/"}
        )