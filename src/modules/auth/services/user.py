from typing import Annotated
from src.modules.users.repository import UserRepository
from fastapi import Depends
from src.modules.auth.schemas import UserLoginSchema,UserRegisterSchema,TokenResponse,AccessTokenPayload,RefreshTokenPayload
from src.core.logger import logger
from src.core.error.exceptions import ValidationException
from src.core.security import password_handler,JWTHandler
from src.core.error.format_error import ERROR_MAPPER
from src.core.error.codes import EMAIL_ALREADY_EXISTS

from src.modules.users.models import User



class UserAuthService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repository = user_repository
        self.logger=logger

    
    
    async def register(self,user_data:UserRegisterSchema) ->TokenResponse:
        existing_user=await self.user_repository.get_by_email(user_data.email)

        if existing_user:
            self.logger.warning(f"Registration failed: Email already registered - {user_data.email}")
            raise ValidationException(
                errors=ERROR_MAPPER[EMAIL_ALREADY_EXISTS]
            )
        
        hashed_password = password_handler.hash(user_data.password)
        created_user=await self.user_repository.create(
            User(hashed_password=hashed_password,
                 **user_data.model_dump(exclude={'hashed_password'}),
                 )
        )

        self.logger.info(f"User registered successfully: user_id={User.id}, email={User.email}")
        tokens=self.generate_token(user_id=created_user.id)

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
            raise


    async def login_user(self,login_data:UserLoginSchema) -> TokenResponse:
        user=self.user_repository.get_by_email(login_data.email)

        if not user:
            self.logger.warning(f"Login failed: Email not found - {login_data.email}")
            raise ValidationException(
                message="Invalid credentials",
                errors={"email": "Email not found."},
            )

        if not password_handler.verify_password(login_data.password,user.hashed_password):
            self.logger.warning(f"Login failed: Incorrect password for email - {login_data.email}")
            raise ValidationException(
                message="Invalid credentials",
                errors={"password": "Incorrect password."},
            )
        
        self.logger.info(f"User logged in successfully: user_id={user.id}, email={user.email}")
        tokens = self.generate_token(user_id=str(user.id))
        return tokens
    

    


  