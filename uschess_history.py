#!/usr/bin/env python3
"""
Fetch complete chess tournament history for a US Chess player
using the ratings-api.uschess.org REST API.

Usage:
    python uschess_history.py <player_id>
    python uschess_history.py <player_id> --output results.json
"""

import json
import sys
import urllib.request
import urllib.error
import argparse

BASE_URL = "https://ratings-api.uschess.org/api/v1/members"
PAGE_SIZE = 100  # API maximum


def fetch_page(player_id: str, offset: int, page_size: int = PAGE_SIZE) -> dict:
    url = f"{BASE_URL}/{player_id}/sections?offset={offset}&pageSize={page_size}"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code} fetching offset {offset}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL error fetching offset {offset}: {e.reason}", file=sys.stderr)
        sys.exit(1)


def fetch_all_tournaments(player_id: str) -> list:
    all_items = []
    offset = 0
    page_num = 1

    while True:
        print(f"  Fetching page {page_num} (offset={offset})...", file=sys.stderr)
        data = fetch_page(player_id, offset)

        items = data.get("items", [])
        all_items.extend(items)

        print(f"    Got {len(items)} tournaments (total so far: {len(all_items)})", file=sys.stderr)

        if not data.get("hasNextPage", False):
            break

        offset += data.get("pageSize", PAGE_SIZE)
        page_num += 1

    return all_items


def main():
    parser = argparse.ArgumentParser(
        description="Fetch complete US Chess tournament history for a player."
    )
    parser.add_argument("player_id", help="US Chess member ID (e.g. 12877028)")
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Write JSON output to FILE instead of stdout",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2; use 0 for compact)",
    )
    args = parser.parse_args()

    print(f"Fetching tournament history for player {args.player_id}...", file=sys.stderr)
    tournaments = fetch_all_tournaments(args.player_id)
    print(f"Done. Total tournaments retrieved: {len(tournaments)}", file=sys.stderr)

    indent = args.indent if args.indent > 0 else None
    output_json = json.dumps(tournaments, indent=indent)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
