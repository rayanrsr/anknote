"""Tests for the main anknote module."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from anknote import __version__, main
from anknote.main import get_args, validate_args, load_custom_prompt, setup_logging


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_main_function_import() -> None:
    """Test that main function can be imported."""
    assert callable(main)


class TestArgParsing:
    """Test command line argument parsing."""

    def test_minimal_args(self) -> None:
        """Test parsing with minimal required arguments."""
        with patch("sys.argv", ["anknote", "test.md"]):
            args = get_args()
            assert args.input_path == "test.md"
            assert args.output == "."
            assert args.model is None  # No default in CLI, comes from config
            assert not args.force_overwrite
            assert not args.in_place
            assert not args.verbose
            assert not args.quiet

    def test_all_args(self) -> None:
        """Test parsing with all arguments."""
        with patch(
            "sys.argv",
            [
                "anknote",
                "notes/",
                "-o",
                "output/",
                "-m",
                "gpt-4",
                "--force-overwrite",
                "--in-place",
                "--verbose",
                "--max-retries",
                "5",
            ],
        ):
            args = get_args()
            assert args.input_path == "notes/"
            assert args.output == "output/"
            assert args.model == "gpt-4"
            assert args.force_overwrite
            assert args.in_place
            assert args.verbose
            assert args.max_retries == 5


class TestValidation:
    """Test argument validation."""

    def test_validate_nonexistent_path(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test validation with non-existent input path."""
        args = MagicMock()
        args.input_path = "/nonexistent/path"
        args.in_place = False
        args.output = "."

        with pytest.raises(SystemExit):
            validate_args(args)

    def test_validate_existing_file(self, tmp_path: Path) -> None:
        """Test validation with existing file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")

        args = MagicMock()
        args.input_path = str(test_file)
        args.in_place = False
        args.output = str(tmp_path)

        # Should not raise
        validate_args(args)


class TestCustomPrompt:
    """Test custom prompt loading."""

    def test_load_default_prompt(self) -> None:
        """Test loading default prompt when no file provided."""
        from anknote.io.write import DEFAULT_PROMPT

        result = load_custom_prompt(None)
        assert result == DEFAULT_PROMPT

    def test_load_custom_prompt_file(self, tmp_path: Path) -> None:
        """Test loading custom prompt from file."""
        prompt_file = tmp_path / "custom_prompt.txt"
        custom_content = "This is a custom prompt for testing."
        prompt_file.write_text(custom_content)

        result = load_custom_prompt(prompt_file)
        assert result == custom_content

    def test_load_empty_prompt_file(self, tmp_path: Path) -> None:
        """Test loading empty prompt file falls back to default."""
        from anknote.io.write import DEFAULT_PROMPT

        prompt_file = tmp_path / "empty_prompt.txt"
        prompt_file.write_text("")

        result = load_custom_prompt(prompt_file)
        assert result == DEFAULT_PROMPT

    def test_load_nonexistent_prompt_file(self) -> None:
        """Test loading non-existent prompt file falls back to default."""
        from anknote.io.write import DEFAULT_PROMPT

        result = load_custom_prompt(Path("/nonexistent/prompt.txt"))
        assert result == DEFAULT_PROMPT


class TestLogging:
    """Test logging configuration."""

    def test_setup_logging_default(self) -> None:
        """Test default logging setup."""
        # This mainly tests that the function doesn't crash
        setup_logging()

    def test_setup_logging_verbose(self) -> None:
        """Test verbose logging setup."""
        setup_logging(verbose=True)

    def test_setup_logging_quiet(self) -> None:
        """Test quiet logging setup."""
        setup_logging(quiet=True)


@patch("anknote.main.retrieve_input")
@patch("anknote.main.generate_and_write_cards")
@patch("anknote.main.console")
class TestMainFunction:
    """Test the main function integration."""

    def test_main_success(
        self,
        mock_console: MagicMock,
        mock_generate: MagicMock,
        mock_retrieve: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test successful main execution."""
        # Create a test markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Note\nThis is a test.")

        # Mock the functions
        mock_retrieve.return_value = [MagicMock()]

        with patch("sys.argv", ["anknote", str(test_file), "--quiet"]):
            main()

        mock_retrieve.assert_called_once()
        mock_generate.assert_called_once()

    def test_main_no_files(
        self,
        mock_console: MagicMock,
        mock_generate: MagicMock,
        mock_retrieve: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test main with no files to process."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")

        mock_retrieve.return_value = []

        with patch("sys.argv", ["anknote", str(test_file)]):
            main()

        mock_retrieve.assert_called_once()
        mock_generate.assert_not_called()

    def test_main_keyboard_interrupt(
        self,
        mock_console: MagicMock,
        mock_generate: MagicMock,
        mock_retrieve: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test main handles keyboard interrupt."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")

        mock_retrieve.side_effect = KeyboardInterrupt()

        with patch("sys.argv", ["anknote", str(test_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 130
