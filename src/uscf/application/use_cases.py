"""Application use cases: orchestration that depends only on ports.

This layer knows the pagination *policy* (keep fetching until there is no next
page) but nothing about HTTP, JSON, or the console.
"""

from __future__ import annotations

from uscf.application.ports import ProgressReporter, TournamentSource
from uscf.domain.models import PlayerHistory, Tournament

DEFAULT_PAGE_SIZE = 100  # US Chess API maximum


def fetch_player_history(
    player_id: str,
    source: TournamentSource,
    reporter: ProgressReporter,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> PlayerHistory:
    """Page through ``source`` and assemble the player's full history."""
    tournaments: list[Tournament] = []
    offset = 0
    page_num = 1

    while True:
        reporter.page_started(page_num, offset)
        page = source.fetch_page(player_id, offset, page_size)
        tournaments.extend(page.items)
        reporter.page_completed(page_num, len(page.items), len(tournaments))

        if not page.has_next_page:
            break

        offset += page.page_size
        page_num += 1

    reporter.finished(len(tournaments))
    return PlayerHistory(player_id=player_id, tournaments=tournaments)
