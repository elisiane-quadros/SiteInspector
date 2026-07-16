from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Ambiente da aplicação
    app_env: str = "development"

    # Endereços do frontend com permissão de chamar a API
    allowed_origins: str = "http://localhost:5173"

    # Tempo máximo para carregamento inicial da página (segundos)
    request_timeout: int = 30

    #Tempo máximo aguardando a estabilização da rede após o carregamento (segundos)
    network_timeout: int = 8

    # Máximo de elementos analisados por página
    max_elements: int = 200

    # Chave da API Groq para geração de relatórios e descrição de imagens
    groq_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_origins_list(self) -> list[str]:
        """Converte a string de origens permitidas em lista."""
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()