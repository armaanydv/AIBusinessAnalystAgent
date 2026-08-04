from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class LLMSettings(BaseAppSettings):
    provider: str = Field(
        default="groq",
        alias="LLM_PROVIDER",
    )

    gemini_api_key: str = Field(
        default="",
        alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        alias="GEMINI_MODEL",
    )

    groq_api_key: str = Field(
        default="",
        alias="GROQ_API_KEY",
    )

    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        alias="GROQ_MODEL",
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


class StorageSettings(BaseAppSettings):
    root_directory: str = Field(
        default="storage/documents",
        alias="STORAGE_ROOT_DIRECTORY",
    )


class Settings:
    def __init__(self) -> None:
        self.llm = LLMSettings()
        self.storage = StorageSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()