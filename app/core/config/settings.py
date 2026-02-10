from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = "app/.env"


settings = Settings()  # type: ignore[call-arg]
