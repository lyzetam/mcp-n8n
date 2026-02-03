"""Pydantic Settings configuration for n8n MCP server."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """n8n API configuration.

    Reads from environment variables with N8N_ prefix or .env file.
    The base_url is computed from protocol + host if not explicitly set.
    """

    host: str = Field(default="localhost:5678", description="n8n host and port")
    protocol: str = Field(default="http", description="n8n protocol (http or https)")
    base_url: Optional[str] = Field(
        default=None,
        description="Full n8n base URL (overrides protocol + host)",
    )
    api_key: str = Field(default="", description="n8n API key")

    model_config = SettingsConfigDict(
        env_prefix="N8N_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def resolved_base_url(self) -> str:
        """Return base_url if set, otherwise compute from protocol + host."""
        if self.base_url:
            return self.base_url
        return f"{self.protocol}://{self.host}"


def get_settings() -> Settings:
    """Get configuration from environment variables or .env file."""
    return Settings()
