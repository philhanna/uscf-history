"""Inbound adapter and composition root: the command-line entry point.

Parses arguments, wires the concrete outbound adapters to the use case's
ports, runs the use case, and maps domain errors to process exit codes.
"""

from __future__ import annotations

import argparse
import sys

from uscf.adapters.outbound.json_writer import JsonHistoryWriter
from uscf.adapters.outbound.stderr_reporter import StderrProgressReporter
from uscf.adapters.outbound.uscf_api import UscfApiGameSource
from uscf.application.use_cases import DEFAULT_PAGE_SIZE, fetch_player_history
from uscf.domain.errors import GameSourceError


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    source = UscfApiGameSource()
    reporter = StderrProgressReporter()
    writer = JsonHistoryWriter(output_path=args.output, indent=args.indent)

    print(
        f"Fetching game history for player {args.player_id}...",
        file=sys.stderr,
    )

    try:
        history = fetch_player_history(
            player_id=args.player_id,
            source=source,
            reporter=reporter,
            page_size=DEFAULT_PAGE_SIZE,
        )
    except GameSourceError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    writer.write(history)
    if args.output:
        print(f"Results written to {args.output}", file=sys.stderr)
    return 0


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch complete US Chess game history for a player."
    )
    parser.add_argument("player_id", help="US Chess member ID (e.g. 12910923)")
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Write JSON output to FILE instead of stdout",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2; use 0 for compact)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
