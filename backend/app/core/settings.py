from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """
    LLM-related configuration.
    """

    api_key: str = Field(alias="GEMINI_API_KEY")
    model: str = Field(
        default="gemini-3.6-flash",
        alias="GEMINI_MODEL",
    )
    temperature: float = Field(
        default=0.2,
        alias="LLM_TEMPERATURE",
    )
    max_tokens: int = Field(
        default=2048,
        alias="LLM_MAX_TOKENS",
    )
    timeout: float = Field(
        default=30.0,
        alias="LLM_TIMEOUT",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class Settings:
    """
    Root application settings.
    """

    def __init__(self):
        self.llm = LLMSettings()


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached application settings instance.
    """
    return Settings()