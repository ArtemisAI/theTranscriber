"""Namespace package for individual route modules."""

# The submodules (`search`, `transcripts`, `playlists`) are imported lazily by
# `app.api.__init__.register_routes` so that importing the package does not
# trigger database/redis connections during unit tests.
