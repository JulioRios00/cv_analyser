"""
Application configuration using Pydantic settings.
This handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "CV Analyzer"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "sqlite:///./cv_analyzer.db"

    # AI Services
    google_api_key: str = ""
    openai_api_key: str = ""
    huggingface_api_key: str = ""

    # File Upload
    max_file_size_mb: int = 10
    upload_dir: str = "./uploads"
    allowed_file_types: List[str] = ["pdf"]

    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    access_token_expire_minutes: int = 30

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024

    def is_ai_configured(self) -> bool:
        """Check if at least one AI service is configured."""
        return bool(self.google_api_key or self.openai_api_key)


# Global settings instance
settings = Settings()
