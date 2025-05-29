"""Tests for the anknote.io modules."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from anknote.io.card import NoteCard
from anknote.io.gather import retrieve_input
from anknote.io.write import (
    save_as_anki,
    split_cards,
    generate_flashcards_for_note,
    FlashcardGenerationError,
    FlashcardParsingError,
)


class TestNoteCard:
    """Test the NoteCard model."""

    def test_create_note_card(self, tmp_path: Path) -> None:
        """Test creating a basic NoteCard."""
        input_path = tmp_path / "test.md"
        card = NoteCard(input_path=input_path, note="Test content")

        assert card.input_path == input_path
        assert card.note == "Test content"
        assert card.output_path is None
        assert card.cards is None

    def test_note_card_str(self, tmp_path: Path) -> None:
        """Test NoteCard string representation."""
        input_path = tmp_path / "test.md"
        card = NoteCard(input_path=input_path, note="Test")

        assert "test.md" in str(card)
        assert "cards=0" in str(card)

        card.cards = [{"prompt": "Q", "answer": "A"}]
        assert "cards=1" in str(card)


class TestRetrieveInput:
    """Test the retrieve_input function."""

    def test_retrieve_single_file(self, tmp_path: Path) -> None:
        """Test retrieving a single markdown file."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Note\nContent here")

        cards = retrieve_input(test_file, tmp_path)

        assert len(cards) == 1
        assert cards[0].input_path == test_file
        assert "Test Note" in cards[0].note
        assert cards[0].output_path == tmp_path / "test.tsv"

    def test_retrieve_directory(self, tmp_path: Path) -> None:
        """Test retrieving files from a directory."""
        # Create test files
        (tmp_path / "note1.md").write_text("# Note 1")
        (tmp_path / "note2.md").write_text("# Note 2")
        (tmp_path / "README.md").write_text("# README")  # Should be skipped
        (tmp_path / "other.txt").write_text("Not markdown")  # Should be skipped

        cards = retrieve_input(tmp_path, tmp_path / "output")

        assert len(cards) == 2
        filenames = [card.input_path.name for card in cards]
        assert "note1.md" in filenames
        assert "note2.md" in filenames
        assert "README.md" not in filenames

    def test_retrieve_nonexistent_path(self) -> None:
        """Test error handling for non-existent path."""
        with pytest.raises(FileNotFoundError):
            retrieve_input(Path("/nonexistent"), Path("."))

    def test_skip_existing_output(self, tmp_path: Path) -> None:
        """Test skipping files with existing output."""
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test")

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        existing_output = output_dir / "test.tsv"
        existing_output.write_text("existing content")

        # Without overwrite - should skip
        cards = retrieve_input(test_file, output_dir, overwrite=False)
        assert len(cards) == 0

        # With overwrite - should include
        cards = retrieve_input(test_file, output_dir, overwrite=True)
        assert len(cards) == 1


class TestSaveAsAnki:
    """Test the save_as_anki function."""

    def test_save_cards(self, tmp_path: Path) -> None:
        """Test saving cards to TSV file."""
        output_file = tmp_path / "test.tsv"
        card = NoteCard(
            input_path=Path("test.md"),
            output_path=output_file,
            cards=[
                {"prompt": "Question 1", "answer": "Answer 1"},
                {"prompt": "Question 2", "answer": "Answer 2"},
            ],
        )

        save_as_anki(card)

        assert output_file.exists()
        content = output_file.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 2
        assert "Question 1\tAnswer 1" in content
        assert "Question 2\tAnswer 2" in content

    def test_save_no_cards(self, tmp_path: Path) -> None:
        """Test saving when no cards are generated."""
        output_file = tmp_path / "test.tsv"
        card = NoteCard(input_path=Path("test.md"), output_path=output_file, cards=[])

        save_as_anki(card)
        # Should not create file for empty cards
        assert not output_file.exists()

    def test_save_no_output_path(self) -> None:
        """Test error when output path is not set."""
        card = NoteCard(input_path=Path("test.md"))

        with pytest.raises(ValueError):
            save_as_anki(card)


class TestSplitCards:
    """Test the split_cards function."""

    def test_split_valid_cards(self) -> None:
        """Test splitting valid card format."""
        content = """
        <START>
        What is Python? <PROMPT-END> A programming language <ANSWER-END>
        What is AI? <PROMPT-END> Artificial Intelligence <ANSWER-END>
        <END>
        """

        cards = split_cards(content)

        assert len(cards) == 2
        assert cards[0]["prompt"] == "What is Python?"
        assert cards[0]["answer"] == "A programming language"
        assert cards[1]["prompt"] == "What is AI?"
        assert cards[1]["answer"] == "Artificial Intelligence"

    def test_split_no_markers(self) -> None:
        """Test splitting content without START/END markers."""
        content = "What is Python? <PROMPT-END> A programming language <ANSWER-END>"

        cards = split_cards(content)

        assert len(cards) == 1
        assert cards[0]["prompt"] == "What is Python?"
        assert cards[0]["answer"] == "A programming language"

    def test_split_malformed_cards(self) -> None:
        """Test handling malformed cards."""
        content = """
        <START>
        Valid card <PROMPT-END> Valid answer <ANSWER-END>
        Invalid card without prompt end
        <END>
        """

        cards = split_cards(content)

        assert len(cards) == 1
        assert cards[0]["prompt"] == "Valid card"

    def test_split_empty_content(self) -> None:
        """Test error handling for empty content."""
        with pytest.raises(FlashcardParsingError):
            split_cards("")

    def test_split_no_valid_cards(self) -> None:
        """Test error when no valid cards found."""
        content = "<START>Invalid content without proper format<END>"

        with pytest.raises(FlashcardParsingError):
            split_cards(content)


class TestGenerateFlashcards:
    """Test flashcard generation."""

    @patch("anknote.io.write.completion")
    def test_generate_success(self, mock_completion: MagicMock, tmp_path: Path) -> None:
        """Test successful flashcard generation."""
        # Mock AI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        <START>
        What is this? <PROMPT-END> A test <ANSWER-END>
        <END>
        """
        mock_completion.return_value = mock_response

        card = NoteCard(
            input_path=tmp_path / "test.md", note="Test content for generation"
        )

        generate_flashcards_for_note(card, "test-model")

        assert card.cards is not None
        assert len(card.cards) == 1
        assert card.cards[0]["prompt"] == "What is this?"
        assert card.cards[0]["answer"] == "A test"

    @patch("anknote.io.write.completion")
    def test_generate_empty_note(
        self, mock_completion: MagicMock, tmp_path: Path
    ) -> None:
        """Test generation with empty note content."""
        card = NoteCard(input_path=tmp_path / "test.md", note="")

        generate_flashcards_for_note(card, "test-model")

        assert card.cards == []
        mock_completion.assert_not_called()

    @patch("anknote.io.write.completion")
    def test_generate_retry_on_failure(
        self, mock_completion: MagicMock, tmp_path: Path
    ) -> None:
        """Test retry mechanism on failure."""
        # First call fails, second succeeds
        mock_completion.side_effect = [
            Exception("API Error"),
            MagicMock(
                choices=[
                    MagicMock(
                        message=MagicMock(
                            content="<START>Q <PROMPT-END> A <ANSWER-END><END>"
                        )
                    )
                ]
            ),
        ]

        card = NoteCard(input_path=tmp_path / "test.md", note="Test content")

        generate_flashcards_for_note(card, "test-model", max_retries=2)

        assert card.cards is not None
        assert len(card.cards) == 1
        assert mock_completion.call_count == 2

    @patch("anknote.io.write.completion")
    def test_generate_max_retries_exceeded(
        self, mock_completion: MagicMock, tmp_path: Path
    ) -> None:
        """Test failure after max retries."""
        mock_completion.side_effect = Exception("Persistent API Error")

        card = NoteCard(input_path=tmp_path / "test.md", note="Test content")

        with pytest.raises(FlashcardGenerationError):
            generate_flashcards_for_note(card, "test-model", max_retries=2)

        assert mock_completion.call_count == 2
