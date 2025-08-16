from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_VERSION: str
    DEBUG: bool
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_MINUTES: int
    REFRESH_TOKEN_EXPIRY_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
