"""API sub-package that wires all routers together."""

from fastapi import FastAPI

from .routes import search, transcripts, playlists


def register_routes(app: FastAPI) -> None:  # pragma: no cover (thin wrapper)
    """Attach routers to the main FastAPI instance."""

    app.include_router(search.router, tags=["search"])
    app.include_router(transcripts.router, tags=["transcripts"])
    app.include_router(playlists.router, tags=["playlists"])
