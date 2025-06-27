from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY:str
    ALGORITHM:str

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()