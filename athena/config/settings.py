from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # 忽略 .env 里多余的变量
    )

    # LLM
    llm_api_key: str
    llm_base_url: str
    llm_main_model: str = "glm-4-flash"
    llm_router_model: str = "glm-4-flash"

    # 数据库
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "athena"
    postgres_password: str = "change_me"
    postgres_db: str = "athena"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str = "change_me"

    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333

    # 监控
    langsmith_api_key: str = ""
    sentry_dsn: str = ""

    # 应用
    app_env: str = "development"
    log_level: str = "INFO"
    max_concurrent_llm_calls: int = 10

    @property
    def postgres_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()