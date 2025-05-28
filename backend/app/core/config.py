"""Application settings & configuration.

Exposes a `settings` singleton – an instance of `Settings` – which loads its
values from environment variables (12-factor).  The object can be imported
from anywhere inside the application:

```
from app.core.config import settings

print(settings.youtube_api_key)
```
"""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict # MODIFIED_LINE
from pydantic import Field, AnyHttpUrl


class Settings(BaseSettings):
    # --- General ---------------------------------------------------------
    environment: str = Field("development")
    debug: bool = Field(True)

    # --- YouTube API ------------------------------------------------------
    youtube_api_key: str = Field("")

    # --- Redis ------------------------------------------------------------
    redis_url: str = Field("redis://redis:6379")

    # --- CORS -------------------------------------------------------------
    allowed_origins: List[AnyHttpUrl] = Field(default=["http://localhost:5173"])

    # --- Misc -------------------------------------------------------------
    log_level: str = Field("INFO")
    cache_ttl_seconds: int = Field(3600, description="Default TTL for cache entries (seconds)")

    # Pydantic-settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",        # Load from .env file if present
        env_file_encoding="utf-8",
        case_sensitive=False,   # Environment variables are usually uppercase
        extra='ignore'          # Ignore extra fields from .env
    )


# Keeping a cached copy so repeated imports are cheap
@lru_cache()
def get_settings() -> Settings:  # pragma: no cover – trivial wrapper
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
