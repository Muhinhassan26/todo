from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class UserLoginSchema(BaseModel):
    email: EmailStr
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
