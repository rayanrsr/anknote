#!/usr/bin/env python3
"""
Anknote - Generate Anki flashcards from markdown notes using AI.
"""

import sys
from pathlib import Path
from typing import Optional
import argparse

from loguru import logger
from rich.console import Console
from rich.panel import Panel

from anknote.io.gather import retrieve_input
from anknote.io.write import generate_and_write_cards, DEFAULT_PROMPT
from anknote.config import (
    load_config,
    apply_env_overrides,
    create_default_config,
)


console = Console()


def setup_logging(
    verbose: bool = False, quiet: bool = False, log_level: Optional[str] = None
) -> None:
    """Configure logging based on verbosity level."""
    logger.remove()  # Remove default handler

    if quiet:
        level = "ERROR"
    elif verbose:
        level = "DEBUG"
    elif log_level:
        level = log_level.upper()
    else:
        level = "INFO"

    if level == "DEBUG":
        format_str = (
            "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
        )
    else:
        format_str = "<level>{level}</level>: {message}"

    logger.add(sys.stderr, level=level, format=format_str)


def validate_args(args: argparse.Namespace) -> None:
    """Validate command line arguments."""
    input_path = Path(args.input_path)

    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input path does not exist: {input_path}")
        sys.exit(1)

    if input_path.is_file() and input_path.suffix not in [".md", ".markdown"]:
        console.print(
            f"[yellow]Warning:[/yellow] Input file is not a markdown file: {input_path}"
        )

    # Validate output path
    output_path = Path(args.input_path if args.in_place else args.output)
    if output_path.is_file():
        console.print(
            f"[red]Error:[/red] Output path is a file, expected directory: {output_path}"
        )
        sys.exit(1)


def get_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="anknote",
        description="Generate Anki flashcards from markdown notes using AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  anknote notes.md                    # Process single file
  anknote ./notes/                    # Process directory
  anknote notes/ -o output/           # Specify output directory
  anknote notes/ --in-place           # Save alongside original files
  anknote notes/ -m "gpt-4"           # Use different AI model
  anknote notes/ --force-overwrite    # Regenerate existing cards

Configuration:
  anknote --init-config               # Create default config file
  anknote --show-config               # Show current configuration
        """,
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        help="Path to markdown file or directory containing markdown files",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Directory to store generated Anki cards (default: current directory)",
        default=".",
    )

    parser.add_argument("-m", "--model", help="AI model name in LiteLLM format")

    parser.add_argument(
        "-f",
        "--force-overwrite",
        help="Regenerate cards even if output files already exist",
        action="store_true",
    )

    parser.add_argument(
        "-i",
        "--in-place",
        help="Save output files alongside input files (ignores --output)",
        action="store_true",
    )

    parser.add_argument(
        "--prompt-file", type=Path, help="Path to custom prompt template file"
    )

    parser.add_argument(
        "--max-retries", type=int, help="Maximum retry attempts for AI generation"
    )

    parser.add_argument(
        "-v", "--verbose", help="Enable verbose logging", action="store_true"
    )

    parser.add_argument("-q", "--quiet", help="Only show errors", action="store_true")

    parser.add_argument("--config", type=Path, help="Path to configuration file")

    parser.add_argument(
        "--init-config", help="Create a default configuration file", action="store_true"
    )

    parser.add_argument(
        "--show-config", help="Show current configuration and exit", action="store_true"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {get_version()}"
    )

    return parser.parse_args()


def get_version() -> str:
    """Get the package version."""
    try:
        from anknote import __version__

        return __version__
    except ImportError:
        return "unknown"


def load_custom_prompt(prompt_file: Optional[Path]) -> str:
    """Load custom prompt from file or return default."""
    if not prompt_file:
        return DEFAULT_PROMPT

    try:
        with prompt_file.open("r", encoding="utf-8") as f:
            custom_prompt = f.read().strip()

        if not custom_prompt:
            logger.warning(f"Empty prompt file: {prompt_file}, using default")
            return DEFAULT_PROMPT

        logger.info(f"Loaded custom prompt from: {prompt_file}")
        return custom_prompt

    except Exception as e:
        logger.error(f"Failed to load prompt file {prompt_file}: {e}")
        logger.info("Using default prompt")
        return DEFAULT_PROMPT


def handle_config_commands(args: argparse.Namespace) -> bool:
    """
    Handle configuration-related commands.

    Returns:
        True if a config command was handled (should exit), False otherwise
    """
    if args.init_config:
        config_content = create_default_config()
        config_path = Path.home() / ".config" / "anknote" / "config.json"

        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(config_content)
            console.print(f"[green]✓[/green] Created default config at: {config_path}")
        except Exception as e:
            console.print(f"[red]Error:[/red] Failed to create config file: {e}")
            sys.exit(1)

        return True

    if args.show_config:
        config = load_config(args.config)
        config = apply_env_overrides(config)

        console.print(
            Panel.fit(
                f"[bold]Current Configuration[/bold]\n\n{create_default_config()}",
                title="Anknote Config",
                border_style="blue",
            )
        )
        return True

    return False


def main() -> None:
    """Main entry point for the anknote CLI."""
    try:
        args = get_args()

        # Handle config commands first
        if handle_config_commands(args):
            return

        # Require input_path for normal operation
        if not args.input_path:
            console.print("[red]Error:[/red] input_path is required")
            sys.exit(1)

        # Load configuration
        config = load_config(args.config)
        config = apply_env_overrides(config)

        # Override config with command line arguments
        if args.model:
            config.model = args.model
        if args.max_retries:
            config.max_retries = args.max_retries

        # Setup logging
        setup_logging(
            verbose=args.verbose, quiet=args.quiet, log_level=config.log_level
        )

        # Validate arguments
        validate_args(args)

        # Show welcome message
        if not args.quiet:
            console.print(
                Panel.fit(
                    "[bold blue]Anknote[/bold blue] - AI-Powered Flashcard Generator",
                    border_style="blue",
                )
            )

        # Determine paths
        input_path = Path(args.input_path)
        output_path = Path(args.input_path if args.in_place else args.output)

        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_path}")
        logger.info(f"Model: {config.model}")

        # Load custom prompt if provided
        prompt = load_custom_prompt(args.prompt_file)

        # Retrieve input files
        logger.info("Scanning for markdown files...")
        cards = retrieve_input(
            input_path=input_path,
            output_path=output_path,
            overwrite=args.force_overwrite,
        )

        if not cards:
            console.print("[yellow]No files to process.[/yellow]")
            return

        # Generate and write cards
        logger.info(f"Processing {len(cards)} files...")
        generate_and_write_cards(
            cards, model=config.model, prompt=prompt, max_retries=config.max_retries
        )

        if not args.quiet:
            console.print("[green]✓ Processing complete![/green]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose if "args" in locals() else False:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == "__main__":
    main()
