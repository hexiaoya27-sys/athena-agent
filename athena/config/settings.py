from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    llm_api_key: str = "placeholder"
    llm_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    llm_main_model: str = "glm-4-flash"
    llm_router_model: str = "glm-4-flash"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "athena"
    postgres_password: str = "athena_pwd"
    postgres_db: str = "athena"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str = "redis_pwd"

    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333

    app_env: str = "development"
    log_level: str = "INFO"
    max_concurrent_llm_calls: int = 10

@lru_cache
def get_settings() -> Settings:
    return Settings()
