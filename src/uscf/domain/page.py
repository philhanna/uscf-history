"""Pure domain model: one page of results from a paginated game source."""

from __future__ import annotations

from dataclasses import dataclass

from uscf.domain.game import Game


@dataclass(frozen=True)
class Page:
    """One page of results from a paginated game source."""

    items: list[Game]
    has_next_page: bool
    page_size: int
