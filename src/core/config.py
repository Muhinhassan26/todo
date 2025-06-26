from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_VERSION: str
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()