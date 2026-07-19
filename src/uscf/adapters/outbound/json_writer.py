"""Outbound adapter: a :class:`HistoryWriter` that emits JSON.

Writes to a file when given a path, otherwise to a stream (stdout by default).
"""

from __future__ import annotations

import json
import sys
from typing import TextIO

from uscf.domain.player_history import PlayerHistory


class JsonHistoryWriter:
    """Serializes a :class:`PlayerHistory` to JSON."""

    def __init__(
        self,
        output_path: str | None = None,
        indent: int = 2,
        stream: TextIO | None = None,
    ) -> None:
        self._output_path = output_path
        self._indent = indent if indent > 0 else None
        self._stream = stream if stream is not None else sys.stdout

    def write(self, history: PlayerHistory) -> None:
        payload = json.dumps(history.to_records(), indent=self._indent)
        if self._output_path:
            with open(self._output_path, "w", encoding="utf-8") as handle:
                handle.write(payload)
        else:
            print(payload, file=self._stream)
