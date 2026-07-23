from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    allowed_origins: str = "http://localhost:5173"

    request_timeout: int = 30

    network_timeout: int = 8

    max_elements: int = 200

    groq_api_key: Optional[str] = None

    groq_report_model: str = "llama-3.3-70b-versatile"

    groq_vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def get_origins_list(self) -> list[str]:
        """Converte a string de origens permitidas em lista."""
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
