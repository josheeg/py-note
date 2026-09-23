"""Capsys-based contract tests for the hello-world CLI."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from main import hello, main


class TestHelloPure:
    """Pure-function unit tests for hello() canonicalization."""

    def test_canonical_world_empty(self) -> None:
        assert hello("") == "Hello, World!"

    def test_canonical_world_whitespace(self) -> None:
        assert hello("   ") == "Hello, World!"

    def test_canonical_trimmed(self) -> None:
        assert hello(" Ada ") == "Hello, Ada!"

    def test_canonical_plain(self) -> None:
        assert hello("Ada") == "Hello, Ada!"


class TestMainCapsys:
    """Capsys-based I/O tests covering the Edge-Case Matrix."""

    def test_bare_run(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main()
        captured = capsys.readouterr()
        assert captured.out == "Hello, World!\n"
        assert captured.err == ""

    def test_custom_name(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main(["--name", "Ada"])
        captured = capsys.readouterr()
        assert captured.out == "Hello, Ada!\n"
        assert captured.err == ""

    def test_empty_name(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main(["--name", ""])
        captured = capsys.readouterr()
        assert captured.out == "Hello, World!\n"
        assert captured.err == ""

    def test_whitespace_name(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main(["--name", "   "])
        captured = capsys.readouterr()
        assert captured.out == "Hello, World!\n"
        assert captured.err == ""

    def test_trimmed_name(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main(["--name", " Ada "])
        captured = capsys.readouterr()
        assert captured.out == "Hello, Ada!\n"
        assert captured.err == ""

    def test_last_one_wins(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        main(["--name", "Ada", "--name", "Belle"])
        captured = capsys.readouterr()
        assert captured.out == "Hello, Belle!\n"
        assert captured.err == ""

    def test_version(self, capsys) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["--version"])
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "main.py 0.1.0\n"
        assert captured.err == ""

    def test_version_precedence(self, capsys) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["--version", "--name", "Ada"])
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert captured.out == "main.py 0.1.0\n"
        assert captured.err == ""

    def test_unknown_flag(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["--bogus"])
        assert excinfo.value.code == 2

    def test_missing_name_value(self: "TestMainCapsys", capsys: pytest.CaptureFixture[str]) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["--name"])
        assert excinfo.value.code == 2

    def test_help(self, capsys) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["-h"])
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "main.py" in captured.out

    def test_help_long(self, capsys) -> None:
        with pytest.raises(SystemExit) as excinfo:
            main(["--help"])
        assert excinfo.value.code == 0
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "main.py" in captured.out