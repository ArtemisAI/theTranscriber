"""Wrapper around `youtube-transcript-api` (placeholder)."""

from __future__ import annotations

from typing import List, Dict


class TranscriptService:  # noqa: D101
    SUPPORTED_FORMATS = {"json", "text", "srt"}

    async def get_transcript(self, video_id: str, fmt: str = "json") -> str:  # noqa: D401
        if fmt not in self.SUPPORTED_FORMATS:
            raise ValueError("Unsupported format")
        raise NotImplementedError

    async def get_many(self, video_ids: List[str], fmt: str = "json") -> Dict[str, str]:  # noqa: D401
        raise NotImplementedError
