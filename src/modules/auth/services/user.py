from typing import Annotated
from src.modules.users.repository import UserRepository
from fastapi import Depends
from src.modules.auth.schemas import LoginData
from fastapi import HTTPException,status
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import jwt
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserAuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository

    

    async def process_login(self, data: LoginData) -> str:
           
        user = await self.user_repository.get_by_email(data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not self.verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

       
        token = self.create_access_token({"sub": str(user.id)})
        return token
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self,password:str):
        return pwd_context.hash(password)
    


    def create_access_token(data: dict, expires_delta: timedelta | None = 30):
        payload= data.copy()
        expire = datetime.utcnow() + timedelta(expires_delta)
        payload.update({"exp": expire})
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)