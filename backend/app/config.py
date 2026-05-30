from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DilsAI Estudos API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    cors_allow_origins: str = (
        "http://localhost:5500,"
        "http://127.0.0.1:5500,"
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://dilson123-tech.github.io"
    )

    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 900
    openai_api_key: str = Field(default="", repr=False)

    model_config = SettingsConfigDict(
        env_file=("backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_allow_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
