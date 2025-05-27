"""/search API endpoint – proxies to the YouTube Data API (placeholder).

Actual implementation will:
1. Validate query params (`q`, `maxResults`, ...).
2. Call the YouTube Data API using the key from settings.
3. Return a filtered JSON response with essential video metadata.

For the repository bootstrap we merely return a `501 Not Implemented` stub so
that the OpenAPI schema is generated and clients are aware of the endpoint.
"""

from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/search")


@router.get("/")
async def search_videos(q: str = Query(..., description="Search query")):
    """Search YouTube videos by keyword (stub)."""

    # TODO: Replace with real implementation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Search endpoint not yet implemented.",
    )
