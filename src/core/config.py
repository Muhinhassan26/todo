from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_VERSION: str
    DEBUG: bool
   
    
settings = Settings()