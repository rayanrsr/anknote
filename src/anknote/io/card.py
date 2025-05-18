from pydantic import BaseModel
from pathlib import Path


class NoteCard(BaseModel):
    input_path: Path | str
    output_path: Path | str | None = ""
    note: str | None = ""
    cards: list[str] | None = None
