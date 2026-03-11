from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    APP_NAME: str = "DEFAULT APP NAME"
    APP_PORT: int = 8999
    APP_VERSION: str = "0.1.0"
    CONVERSATION_MODEL: str = "gpt-4.1"

settings = Settings()
