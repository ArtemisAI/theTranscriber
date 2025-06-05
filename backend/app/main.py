"""FastAPI application factory & entry-point."""

from fastapi import FastAPI
from mangum import Mangum

from app.api import register_routes
from app.core.config import settings
from app.utils.logger import configure_logging


def create_app() -> FastAPI:  # noqa: D401
    """Build and configure the FastAPI application."""

    configure_logging(settings.log_level)

    app = FastAPI(
        title="YouTube Transcript Retrieval Service",
        version="0.1.0",
        debug=settings.debug,
    )

    # Register application routers
    register_routes(app)

    # Health check
    @app.get("/health", tags=["system"])
    async def health():  # noqa: D401
        return {"status": "ok"}

    return app


# Singleton instance used by Uvicorn / tests
app = create_app()

# This is the handler Netlify will use
handler = Mangum(app)
