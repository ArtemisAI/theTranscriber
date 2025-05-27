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

from pydantic import BaseSettings, Field, AnyHttpUrl


class Settings(BaseSettings):
    # --- General ---------------------------------------------------------
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")

    # --- YouTube API ------------------------------------------------------
    youtube_api_key: str = Field("", env="YOUTUBE_API_KEY")

    # --- Redis ------------------------------------------------------------
    redis_url: str = Field("redis://redis:6379", env="REDIS_URL")

    # --- CORS -------------------------------------------------------------
    allowed_origins: List[AnyHttpUrl] = Field(default=["http://localhost:5173"], env="ALLOWED_ORIGINS")

    # --- Misc -------------------------------------------------------------
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        case_sensitive = False


# Keeping a cached copy so repeated imports are cheap
@lru_cache()
def get_settings() -> Settings:  # pragma: no cover – trivial wrapper
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
