"""Domain-level exceptions, independent of any adapter technology."""

from __future__ import annotations


class GameSourceError(Exception):
    """Raised when a game source cannot deliver the requested data."""
