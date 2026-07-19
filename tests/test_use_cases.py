# tests.test_use_cases
"""Use-case tests driven entirely through ports — no network required."""

from __future__ import annotations

import pytest

from uscf.adapters.outbound.stderr_reporter import SilentProgressReporter
from uscf.application.use_cases import fetch_player_history
from uscf.domain.errors import GameSourceError
from uscf.domain.models import Game, Page


class FakeGameSource:
    """In-memory :class:`GameSource` returning pre-canned pages."""

    def __init__(self, pages: list[Page]) -> None:
        self._pages = pages
        self.calls: list[tuple[int, int]] = []

    def fetch_page(self, player_id: str, offset: int, page_size: int) -> Page:
        self.calls.append((offset, page_size))
        return self._pages[len(self.calls) - 1]


def _page(count: int, has_next: bool, page_size: int = 100) -> Page:
    items = [Game(raw={"n": i}) for i in range(count)]
    return Page(items=items, has_next_page=has_next, page_size=page_size)


def test_single_page_history():
    source = FakeGameSource([_page(3, has_next=False)])

    history = fetch_player_history("123", source, SilentProgressReporter())

    assert history.player_id == "123"
    assert len(history.games) == 3
    assert source.calls == [(0, 100)]


def test_paginates_until_no_next_page():
    source = FakeGameSource(
        [_page(100, has_next=True), _page(40, has_next=False)]
    )

    history = fetch_player_history("123", source, SilentProgressReporter())

    assert len(history.games) == 140
    assert source.calls == [(0, 100), (100, 100)]


def test_source_error_propagates():
    class BrokenSource:
        def fetch_page(self, player_id, offset, page_size):
            raise GameSourceError("boom")

    with pytest.raises(GameSourceError):
        fetch_player_history("123", BrokenSource(), SilentProgressReporter())
