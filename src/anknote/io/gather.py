from pathlib import Path
from loguru import logger
from anknote.io.card import NoteCard


def retrieve_input(
    input_path: Path, output_path: Path, overwrite: bool = False
) -> list[NoteCard]:
    cards: list[NoteCard] = []
    if input_path.is_dir():
        all_markdowns = input_path.rglob("**.md")
        for file_path in all_markdowns:
            content = open(file_path, "r").read()
            cards.append(NoteCard(input_path=file_path, note=content))

    else:
        content = open(input_path, "r").read()
        cards.append(NoteCard(input_path=input_path, note=content))
    valid_cards: list[NoteCard] = []
    for nc in cards:
        card_save_path = output_path / nc.input_path.relative_to(input_path)
        card_save_path = card_save_path.with_suffix(".tsv")
        nc.output_path = card_save_path
        if nc.output_path.exists() and not overwrite:
            logger.debug(f"Skipping {nc.input_path} as it already exists.")
        else:
            valid_cards.append(nc)
    return valid_cards
