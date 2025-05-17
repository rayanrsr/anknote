from loguru import logger
from pathlib import Path


def retrieve_input(input_path: Path) -> dict:
    print(input_path.glob("*"))
    if input_path.is_dir():
        logger.debug("Input path is a directory")

    else:
        logger.debug("Input path is a file")
