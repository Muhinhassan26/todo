from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

# class LoginData(BaseModel):
#     username: str 
#     email:EmailStr
#     password: str



class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    access_token_expire: datetime | None = None


class AccessTokenPayload(BaseModel):
    user_id: str
    exp: datetime | None = None
    sub: str = "access"


class RefreshTokenPayload(BaseModel):
    user_id: str
    exp: datetime | None = None
    sub: str = "refresh"