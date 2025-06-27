from pydantic import BaseModel,EmailStr

class LoginData(BaseModel):
    username: str 
    email:EmailStr
    password: str