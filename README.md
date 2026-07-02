# uscf-history

Uses the REST API provided by the U. S. Chess Federation to download the
lifetime tournament history of a player.

See the [USCF Swagger Page](https://ratings-api.uschess.org/swagger/index.html) for details of the API.

## Install

Requires Python 3.10 or newer and git.

### 1. Clone the repository

```bash
git clone https://github.com/philhanna/uscf-history.git
cd uscf-history
```

### 2. Create and activate a virtual environment

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install the application

```bash
pip install .
```

For development (editable install plus test dependencies), use `pip install -e .`.

## Usage

```bash
uscf <player_id>                      # JSON to stdout
uscf <player_id> --output history.json
uscf <player_id> --indent 0           # compact JSON
```

Equivalent invocation:

```bash
python -m uscf <player_id>
```

Progress is written to stderr; the JSON result to stdout (or `--output` file).

## Architecture

The project follows a hexagonal (ports and adapters) design. The use case
depends only on ports (`typing.Protocol`); concrete I/O lives in adapters.

```
╔════════════════════════════════════════════════════════════╗
║  Driving Side (Inbound)                                    ║
║    uscf.adapters.inbound.cli : main()  ← argparse          ║
╚════════════════════════════════════════════════════════════╝
                          │ calls
                          ▼
╔════════════════════════════════════════════════════════════╗
║  Application Layer                                         ║
║    fetch_player_history(...)                               ║
║    ports: TournamentSource, HistoryWriter, ProgressReporter║
╚════════════════════════════════════════════════════════════╝
                          │ implemented by
                          ▼
╔════════════════════════════════════════════════════════════╗
║  Driven Side (Outbound Adapters)                           ║
║    UscfApiTournamentSource (urllib HTTP)                   ║
║    JsonHistoryWriter (file/stdout)                         ║
║    StderrProgressReporter                                  ║
╚════════════════════════════════════════════════════════════╝
                          │ uses
                          ▼
╔════════════════════════════════════════════════════════════╗
║  Domain Layer                                              ║
║    Tournament, Page, PlayerHistory, TournamentSourceError  ║
╚════════════════════════════════════════════════════════════╝
```

Data flow: CLI parses args → wires adapters to ports → `fetch_player_history`
pages through `TournamentSource` → assembles a `PlayerHistory` → `HistoryWriter`
emits JSON. The use case may import ports and domain types only — never adapters.

## Development

```bash
pip install pytest
pytest
```
