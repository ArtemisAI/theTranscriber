"""/transcripts API endpoint – fetches transcripts for one or many videos.

The final version will:
* Accept `id` query param (single or comma-separated list) or JSON body with
  array of IDs (POST variant).
* Parse `format` (text/json/srt) and dispatch to `app.services.transcript_service`.
* Leverage Redis caching for performance.

Currently returns *501 Not Implemented* placeholders.
"""

from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/transcripts")


@router.get("/")
async def get_transcript(
    id: str = Query(..., description="One or more YouTube video IDs"),
    format: str = Query("json", regex="^(json|text|srt)$"),  # noqa: A003
):
    """Retrieve transcript(s) for given video ID(s) (stub)."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Transcript endpoint not yet implemented.",
    )
