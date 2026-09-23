"""A Python CLI hello world program."""

import argparse

__version__ = "0.1.0"


def hello(name: str) -> str:
    """Return a greeting for name, stripping whitespace and falling back to World when empty."""
    return f"Hello, {name.strip() or 'World'}!"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    args = parser.parse_args(argv)
    print(hello(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
