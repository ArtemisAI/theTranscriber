"""Async YouTube Data API v3 client (placeholder).

Will encapsulate authentication, quota monitoring, paging, and error
handling.  The class is intentionally **not** implemented yet; call sites
should import the class and expect `NotImplementedError` until Phase 2.
"""

from __future__ import annotations


class YouTubeClient:  # noqa: D101
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search(self, query: str, max_results: int = 25):  # noqa: D401
        raise NotImplementedError

    async def playlist_items(self, playlist_id: str):  # noqa: D401
        raise NotImplementedError
