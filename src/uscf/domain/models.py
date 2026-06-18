"""Pure domain models for US Chess tournament history.

These types have no knowledge of HTTP, JSON files, argparse, or any other
infrastructure concern. They describe *what* the application works with.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PlayerHistory:
    """The complete tournament history retrieved for a single player."""

    player_id: str
    tournaments: list[Tournament]

    def to_records(self) -> list[dict[str, Any]]:
        """Serialize back to the list-of-records shape returned by the API."""
        return [tournament.to_dict() for tournament in self.tournaments]


@dataclass(frozen=True)
class Tournament:
    """A single tournament section a player competed in.

    The raw record from the source is preserved verbatim so that output is
    lossless; richer typed accessors can be added here as needs grow.
    """

    raw: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.raw)


@dataclass(frozen=True)
class Page:
    """One page of results from a paginated tournament source."""

    items: list[Tournament]
    has_next_page: bool
    page_size: int
