from pydantic import BaseClass


class NoteCard(BaseClass):
    input_path: str
    output_path: str | None = ""
    note: str | None = ""
    cards: list[str]
