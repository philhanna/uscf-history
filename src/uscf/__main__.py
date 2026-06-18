"""Enable ``python -m uscf``."""

from uscf.adapters.inbound.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
