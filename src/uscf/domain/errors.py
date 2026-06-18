"""Domain-level exceptions, independent of any adapter technology."""

from __future__ import annotations


class TournamentSourceError(Exception):
    """Raised when a tournament source cannot deliver the requested data."""
