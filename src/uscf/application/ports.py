"""Ports: the abstract boundaries the application depends on.

Each port is a ``typing.Protocol`` so that any object with a matching shape
satisfies it — no inheritance or registration required. Outbound adapters in
``uscf.adapters.outbound`` provide concrete implementations.
"""

from __future__ import annotations

from typing import Protocol

from uscf.domain.models import Page, PlayerHistory


class GameSource(Protocol):
    """Driven port: a paginated source of a player's games."""

    def fetch_page(self, player_id: str, offset: int, page_size: int) -> Page:
        """Return one page of games starting at ``offset``.

        Implementations should raise
        :class:`uscf.domain.errors.GameSourceError` on failure.
        """
        ...


class HistoryWriter(Protocol):
    """Driven port: a sink that persists or emits a completed history."""

    def write(self, history: PlayerHistory) -> None:
        ...


class ProgressReporter(Protocol):
    """Driven port: receives progress updates while paging through results."""

    def page_started(self, page_num: int, offset: int) -> None:
        ...

    def page_completed(self, page_num: int, page_count: int, total: int) -> None:
        ...

    def finished(self, total: int) -> None:
        ...
