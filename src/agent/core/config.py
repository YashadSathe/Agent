from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "AI Agent Platform"
    environment: str = "development"
    debug: bool = True

    #LLM Configureation
    openrouter_api_key : Optional[SecretStr] = None
    default_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "UTF-8",
        extra = "ignore"
        )
    
settings = Settings()
    