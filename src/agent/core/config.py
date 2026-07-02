from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Agent Platform"
    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "UTF-8",
        extra = "ignore"
        )
    
settings = Settings()
    