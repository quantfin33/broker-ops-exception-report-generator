"""Module entrypoint for `python -m broker_ops_report`."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
