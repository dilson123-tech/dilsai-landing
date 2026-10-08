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
    # Modelo com visão para "Resolver pela foto". Vazio = usa llm_model.
    llm_vision_model: str = ""
    # Saída é o que mais pesa no tempo de resposta; 900 cobre a explicação passo a passo.
    llm_vision_max_tokens: int = 900
    # "high" mantém letras pequenas legíveis; "auto" pode cair para baixa resolução (512 px).
    llm_vision_detail: str = "high"
    openai_api_key: str = Field(default="", repr=False)

    rate_limit_enabled: bool = True
    rate_limit_window_seconds: int = 60
    rate_limit_chat_per_minute: int = 20
    rate_limit_material_per_minute: int = 8

    model_config = SettingsConfigDict(
        env_file=("backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def vision_model(self) -> str:
        return self.llm_vision_model.strip() or self.llm_model

    @property
    def vision_detail(self) -> str:
        detail = self.llm_vision_detail.strip().lower()
        return detail if detail in {"low", "high", "auto"} else "high"

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
