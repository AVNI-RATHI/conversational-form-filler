"""Configuration management for the Conversational Form Filler application."""

from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = "sk-test-default"
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7

    # Database Configuration
    database_url: str = "sqlite:///./form_filler.db"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_echo: bool = False

    # Application Settings
    log_level: str = "INFO"
    debug: bool = False

    # Agent Configuration
    max_agent_iterations: int = 10
    agent_timeout: int = 300
    confidence_threshold: float = 0.8

    # Session Configuration
    session_expiry_hours: int = 24
    max_concurrent_sessions: int = 1000

    # Form Configuration
    required_slots: list = ["name", "email", "phone"]
    optional_slots: list = ["company", "address", "notes"]

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()

settings = get_settings()
