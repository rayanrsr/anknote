from pathlib import Path
from typing import List
from loguru import logger
from anknote.io.card import NoteCard


def retrieve_input(
    input_path: Path, output_path: Path, overwrite: bool = False
) -> List[NoteCard]:
    """
    Retrieve markdown files and create NoteCard objects.

    Args:
        input_path: Path to input file or directory
        output_path: Path where output files will be saved
        overwrite: Whether to overwrite existing output files

    Returns:
        List of NoteCard objects ready for processing

    Raises:
        FileNotFoundError: If input_path doesn't exist
        PermissionError: If unable to read input files
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    cards: List[NoteCard] = []

    try:
        if input_path.is_dir():
            all_markdowns = list(input_path.rglob("*.md"))
            logger.info(f"Found {len(all_markdowns)} markdown files in {input_path}")

            for file_path in all_markdowns:
                if file_path.name == "README.md":
                    logger.debug(f"Skipping README.md: {file_path}")
                    continue

                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    cards.append(
                        NoteCard(
                            input_path=file_path,
                            note=content,
                            output_path=None,
                            cards=None,
                        )
                    )
                except (UnicodeDecodeError, PermissionError) as e:
                    logger.warning(f"Failed to read {file_path}: {e}")
                    continue
        else:
            if input_path.suffix != ".md":
                logger.warning(f"Input file is not a markdown file: {input_path}")

            if input_path.name != "README.md":
                try:
                    with input_path.open("r", encoding="utf-8") as f:
                        content = f.read()
                    cards.append(
                        NoteCard(
                            input_path=input_path,
                            note=content,
                            output_path=None,
                            cards=None,
                        )
                    )
                except (UnicodeDecodeError, PermissionError) as e:
                    logger.error(f"Failed to read {input_path}: {e}")
                    raise
    except Exception as e:
        logger.error(f"Error processing input path {input_path}: {e}")
        raise

    # Filter cards based on existing output files
    valid_cards: List[NoteCard] = []
    for nc in cards:
        try:
            # Calculate relative path properly
            if input_path.is_dir():
                relative_path = nc.input_path.relative_to(input_path)
            else:
                relative_path = Path(nc.input_path.name)

            card_save_path = Path(output_path) / relative_path
            card_save_path = card_save_path.with_suffix(".tsv")
            nc.output_path = card_save_path

            if nc.output_path.exists() and not overwrite:
                logger.debug(
                    f"Skipping {nc.input_path} as output already exists: {nc.output_path}"
                )
            else:
                valid_cards.append(nc)
        except ValueError as e:
            logger.error(f"Failed to calculate relative path for {nc.input_path}: {e}")
            continue

    logger.info(
        f"Processing {len(valid_cards)} files (skipped {len(cards) - len(valid_cards)})"
    )
    return valid_cards
