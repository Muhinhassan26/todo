from fastapi import Request, Depends, HTTPException, status
from src.core.security import JWTHandler
from src.core.logger import logger

def get_current_user_id(request: Request) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Missing or invalid Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing or malformed. Use Bearer token in header."
        )

    token = auth_header.split(" ")[1]

    try:
        payload = JWTHandler.decode(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing user ID."
            )
        return int(user_id)

    except Exception as e:
        logger.error(f"Access token decoding failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token is invalid or expired."
        )


def require_login(request: Request) -> int:
    return get_current_user_id(request)
