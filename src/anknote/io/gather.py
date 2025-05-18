from loguru import logger
from pathlib import Path


def retrieve_input(input_path: Path) -> dict:
    if input_path.is_dir():
        logger.debug("Input path is a directory")
        all_markdowns = input_path.rglob("**.md")
        logger.debug(all_markdowns)
        for file in all_markdowns:
            logger.debug(file)

    else:
        logger.debug("Input path is a file")
