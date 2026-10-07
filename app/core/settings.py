from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_TOKEN_EXPIRE: int
    JWT_ALGORITHIM: str
    JWT_SECRET_KEY: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
