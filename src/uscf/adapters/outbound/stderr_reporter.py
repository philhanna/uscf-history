"""Outbound adapter: a :class:`ProgressReporter` that writes to a stream.

Mirrors the original script's stderr progress messages.
"""

from __future__ import annotations

import sys
from typing import TextIO


class StderrProgressReporter:
    """Reports paging progress to stderr (or any text stream)."""

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream = stream if stream is not None else sys.stderr

    def page_started(self, page_num: int, offset: int) -> None:
        print(f"  Fetching page {page_num} (offset={offset})...", file=self._stream)

    def page_completed(self, page_num: int, page_count: int, total: int) -> None:
        print(
            f"    Got {page_count} games (total so far: {total})",
            file=self._stream,
        )

    def finished(self, total: int) -> None:
        print(f"Done. Total games retrieved: {total}", file=self._stream)


class SilentProgressReporter:
    """A no-op reporter, useful in tests and non-interactive contexts."""

    def page_started(self, page_num: int, offset: int) -> None:
        ...

    def page_completed(self, page_num: int, page_count: int, total: int) -> None:
        ...

    def finished(self, total: int) -> None:
        ...
