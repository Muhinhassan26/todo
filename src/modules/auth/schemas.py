from pydantic import BaseModel,EmailStr
from datetime import datetime

class LoginData(BaseModel):
    username: str 
    email:EmailStr
    password: str



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