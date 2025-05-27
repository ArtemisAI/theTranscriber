"""Top-level package for the FastAPI application.

This module intentionally left almost empty – application construction is
performed in `app.main` to avoid import cycles (e.g. when Celery workers or
other external services need to import just the settings without triggering
the whole ASGI stack).
"""

__all__ = [
    "__version__",
]

__version__ = "0.1.0"
