from fastapi import Request, Depends, HTTPException, status
from src.core.security import JWTHandler
from fastapi.security import OAuth2PasswordBearer
from src.core.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user/login/")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    

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


