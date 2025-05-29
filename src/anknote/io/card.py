from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path
from typing import Optional


class NoteCard(BaseModel):
    """Represents a note card with input/output paths and generated flashcards."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    input_path: Path = Field(..., description="Path to the input markdown file")
    output_path: Optional[Path] = Field(
        None, description="Path where the TSV file will be saved"
    )
    note: str = Field(default="", description="Content of the markdown note")
    cards: Optional[list[dict[str, str]]] = Field(
        None, description="Generated flashcards"
    )

    def __str__(self) -> str:
        return f"NoteCard(input={self.input_path.name}, cards={len(self.cards) if self.cards else 0})"
