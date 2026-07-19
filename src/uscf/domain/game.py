"""Pure domain model: a single game a player competed in.

This type has no knowledge of HTTP, JSON files, argparse, or any other
infrastructure concern. It describes *what* the application works with.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Game:
    """A single game a player competed in.

    The raw record from the source is preserved verbatim so that output is
    lossless; richer typed accessors can be added here as needs grow.
    """

    raw: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.raw)
