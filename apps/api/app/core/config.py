from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Guia Produto Radar"
    project_slug: str = "guia-produto-radar-api"
    app_version: str = "0.1.0"
    app_env: str = Field(default="local", validation_alias="APP_ENV")
    database_url: str = Field(
        default="postgresql+psycopg://gp_local_user:gp_local_password_change_me@postgres:5432/guia_produto_radar",
        validation_alias="DATABASE_URL",
    )
    redis_url: str = Field(
        default="redis://redis:6379/0",
        validation_alias="REDIS_URL",
    )
    admin_cors_origins: str = Field(
        default="http://localhost:18090,http://127.0.0.1:18090",
        validation_alias="ADMIN_CORS_ORIGINS",
    )
    admin_auth_enabled: bool = Field(
        default=False,
        validation_alias="ADMIN_AUTH_ENABLED",
    )
    admin_api_token: str = Field(
        default="",
        validation_alias="ADMIN_API_TOKEN",
    )

    @property
    def admin_cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.admin_cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def has_configured_admin_token(self) -> bool:
        token = self.admin_api_token.strip()
        return bool(token) and not token.lower().startswith("change-me")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
