from pydantic import BaseModel,EmailStr,Field,model_validator
from datetime import datetime



class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    confirm_password:str=Field(..., min_length=6, max_length=128)

    @model_validator(mode="after")
    def passwords_match(cls, values):
        pw = values.get("password")
        confirm_pw = values.get("confirm_password")
        if pw != confirm_pw:
            raise ValueError("Passwords do not match")
        return values


class UserLoginSchema(BaseModel):
    email:EmailStr
    password:str=Field(..., min_length=6, max_length=128)



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