from pydantic import BaseModel
from pathlib import Path


class NoteCard(BaseModel):
    input_path: Path
    output_path: Path | None = None
    note: str | None = ""
    cards: list[dict[str, str]] | None = None
