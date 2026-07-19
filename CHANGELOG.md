# Changelog

## [1.0.0] - 2026-07-19

### Changed
- Switched player history source from tournaments to individual
  games: fetches `{player_id}/games` instead of `{player_id}/sections`,
  renaming Tournament terminology to Game throughout the domain,
  application, and adapter layers.
- Split domain models into one file per class (`game.py`, `page.py`,
  `player_history.py`) instead of a single `models.py`.
- Updated README with the refactored architecture and
  platform-specific install instructions.
- Ignored `.json` files from test runs.
- Changed sample player ID in CLI help text.

## [0.1.0] - 2026-06-17

### Changed
- Restructured the single-file `uschess_history.py` script into a hexagonal
  (ports and adapters) `uscf` package under a `src/` layout.
- Network, JSON, and progress I/O are now outbound adapters behind
  `typing.Protocol` ports (`TournamentSource`, `HistoryWriter`,
  `ProgressReporter`); the `fetch_player_history` use case is pure.
- HTTP/URL failures now surface as the domain exception
  `TournamentSourceError`, which the CLI maps to exit code 1.

### Added
- `pyproject.toml` with a `uscf` console-script entry point and pytest config.
- `python -m uscf` entry point.
- Pytest suite covering single-page, multi-page pagination, and error
  propagation via an in-memory fake source (no network).
