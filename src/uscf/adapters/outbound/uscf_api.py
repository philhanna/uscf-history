"""Outbound adapter: a :class:`TournamentSource` backed by the US Chess REST API.

Implements the driven port using ``urllib`` and translates transport failures
into the domain's :class:`TournamentSourceError`.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from uscf.application.use_cases import DEFAULT_PAGE_SIZE
from uscf.domain.errors import TournamentSourceError
from uscf.domain.models import Page, Tournament

DEFAULT_BASE_URL = "https://ratings-api.uschess.org/api/v1/members"


class UscfApiTournamentSource:
    """Fetches tournament games from ratings-api.uschess.org."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self._base_url = base_url.rstrip("/")

    def fetch_page(
        self, player_id: str, offset: int, page_size: int = DEFAULT_PAGE_SIZE
    ) -> Page:
        url = (
            f"{self._base_url}/{player_id}/games"
            f"?offset={offset}&pageSize={page_size}"
        )
        data = self._get_json(url, offset)
        items = [Tournament(raw=record) for record in data.get("items", [])]
        return Page(
            items=items,
            has_next_page=bool(data.get("hasNextPage", False)),
            page_size=int(data.get("pageSize", page_size)),
        )

    def _get_json(self, url: str, offset: int) -> dict:
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            raise TournamentSourceError(
                f"HTTP error {exc.code} fetching offset {offset}: {exc.reason}"
            ) from exc
        except urllib.error.URLError as exc:
            raise TournamentSourceError(
                f"URL error fetching offset {offset}: {exc.reason}"
            ) from exc
