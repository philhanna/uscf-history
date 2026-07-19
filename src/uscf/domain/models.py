"""Pure domain models for US Chess game history.

These types have no knowledge of HTTP, JSON files, argparse, or any other
infrastructure concern. They describe *what* the application works with.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PlayerHistory:
    """The complete game history retrieved for a single player."""

    player_id: str
    games: list[Game]

    def to_records(self) -> list[dict[str, Any]]:
        """Serialize back to the list-of-records shape returned by the API."""
        return [game.to_dict() for game in self.games]


@dataclass(frozen=True)
class Game:
    """A single game a player competed in.

    The raw record from the source is preserved verbatim so that output is
    lossless; richer typed accessors can be added here as needs grow.
    """

    raw: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.raw)


@dataclass(frozen=True)
class Page:
    """One page of results from a paginated game source."""

    items: list[Game]
    has_next_page: bool
    page_size: int
