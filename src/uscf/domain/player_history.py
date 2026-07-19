"""Pure domain model: the complete game history for a single player."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from uscf.domain.game import Game


@dataclass(frozen=True)
class PlayerHistory:
    """The complete game history retrieved for a single player."""

    player_id: str
    games: list[Game]

    def to_records(self) -> list[dict[str, Any]]:
        """Serialize back to the list-of-records shape returned by the API."""
        return [game.to_dict() for game in self.games]
