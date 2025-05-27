from __future__ import annotations

"""Pydantic model representing minimal YouTube video metadata (placeholder)."""

from pydantic import BaseModel, Field


class Video(BaseModel):  # noqa: D101
    video_id: str = Field(..., alias="id")
    title: str
    description: str | None = None
    published_at: str | None = None  # ISO date string; customise later
