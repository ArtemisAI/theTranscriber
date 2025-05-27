"""/playlists/{playlist_id}/transcripts endpoint (placeholder)."""

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/playlists")


@router.get("/{playlist_id}/transcripts")
async def playlist_transcripts(playlist_id: str):  # noqa: D401
    """Fetch transcripts for all videos in a playlist (stub)."""

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Playlist transcript endpoint not yet implemented.",
    )
