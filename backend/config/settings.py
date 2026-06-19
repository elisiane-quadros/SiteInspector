from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Ambiente da aplicação
    app_env: str = "development"

    # Endereços do frontend com permissão de chamar a API
    allowed_origins: str = "http://localhost:5173"

    request_timeout: int = 30
    max_elements: int = 200
    groq_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def get_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

@lru_cache
def get_settings() -> Settings:
    return Settings()