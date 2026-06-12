from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://postgres:myadmin@localhost:5432/crm_dev"
    test_database_url: str = "postgresql://postgres:myadmin@localhost:5432/crm_test"
    secret_key: str = "change-me-in-production-at-least-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    web_origin: str = "http://localhost:5173"


settings = Settings()
