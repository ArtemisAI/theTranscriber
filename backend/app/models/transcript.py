from __future__ import annotations

"""Pydantic model for transcript snippets (placeholder)."""

from pydantic import BaseModel


class TranscriptSnippet(BaseModel):  # noqa: D101
    text: str
    start: float
    duration: float


class TranscriptResponse(BaseModel):  # noqa: D101
    video_id: str
    snippets: list[TranscriptSnippet]
