from typing import overload
from anknote.io.gather import retrieve_input
from anknote.io.write import generate_and_write_cards

from pathlib import Path
import argparse

from loguru import logger


def get_args():
    parser = argparse.ArgumentParser(
        prog="anknote", description="Generate Anki Cards from a notes folder."
    )
    parser.add_argument("input_path")
    parser.add_argument(
        "-o", "--output", help="Where to store generated Anki cards.", default="."
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Model name to use (following LiteLLM expected format).",
        default="gemini/gemini-2.0-flash-lite",
    )
    parser.add_argument(
        "-s",
        "--save-format",
        help="Which format to save in the output folder anki cards.",
    )
    parser.add_argument(
        "-f",
        "--force-overwrite",
        help="Re-compute all files even already done ones.",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-i",
        "--in-place",
        help="Makes the output_path==input_path.",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = get_args()
    output_path = args.input_path if args.in_place else args.output
    cards = retrieve_input(
        input_path=Path(args.input_path),
        output_path=output_path,
        overwrite=args.force_overwrite,
    )
    generate_and_write_cards(
        cards,
        model=args.model,
    )


if __name__ == "__main__":
    main()
