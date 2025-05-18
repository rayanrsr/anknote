from loguru import logger
from pathlib import Path
from anknote.io.card import NoteCard


def retrieve_input(input_path: Path) -> list[NoteCard]:
    cards: list[NoteCard] = []
    if input_path.is_dir():
        logger.debug("Input path is a directory")
        all_markdowns = input_path.rglob("**.md")
        for file_path in all_markdowns:
            content = open(file_path, "r").read()
            cards.append(NoteCard(input_path=file_path, note=content))

    else:
        logger.debug("Input path is a file")
        content = open(input_path, "r").read()
        cards.append(NoteCard(input_path=input_path, note=content))
    return cards
