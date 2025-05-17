from anknote.io.gather import retrieve_input

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
    return parser.parse_args()


def main():
    args = get_args()
    logger.debug(f"Running Anknote with the following arguments:\n{args}")
    retrieve_input(input_path=args.input_path)


if __name__ == "__main__":
    main()
