from typing import List, Dict, Optional
import re

from litellm import completion
from loguru import logger
from anknote.io.card import NoteCard
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
)

# Default prompt for generating flashcards
DEFAULT_PROMPT = """You are generating Anki flashcards for a user to retain knowledge from their knowledge base. The user text will be a part of their knowledge base notes, and you need to take key concepts and questions for them to remember. Be selective and only take important information. Be concise and clear.

Instructions to create a deck of flashcards:
- Create a list of flash cards.
- Keep the flashcards simple, clear, and focused on the most important information.
- Use simple and direct language to make the cards easy to read and understand.
- Don't include obvious knowledge or irrelevant formulas. Focus on recalling conceptual links or ideas, and put in [] random comments from the notes that seem to enhance the flashcard idea, so that I can see more info when I do my flashcards
- Focus on intuitions and non trivial ideas rather than just facts or simple definitions. This is important.
- Directly write all the cards without repeating the initial text/note.
- Only write the prompt (questions) and the answers, nothing else.
- The list of cards should start with <START> and end with <END>.
- Don't put any line breaks (\\n) in the questions or the answers.

The format of a single flashcard is something like this example `What is a GPU? <PROMPT-END> It is a computing unit dedicated to tensors and .. <ANSWER-END>` for each new line.

Actual user's text you have to transform:
"""


class FlashcardGenerationError(Exception):
    """Raised when flashcard generation fails."""

    pass


class FlashcardParsingError(Exception):
    """Raised when parsing AI response fails."""

    pass


def save_as_anki(note_card: NoteCard) -> None:
    """
    Save flashcards to a TSV file for Anki import.

    Args:
        note_card: NoteCard with generated flashcards

    Raises:
        OSError: If unable to create directory or write file
    """
    if not note_card.output_path:
        raise ValueError("Output path not set for note card")

    if not note_card.cards:
        logger.warning(f"No cards generated for {note_card.input_path}")
        return

    try:
        note_card.output_path.parent.mkdir(parents=True, exist_ok=True)

        with note_card.output_path.open("w", encoding="utf-8") as f:
            for card in note_card.cards:
                # Escape tabs and newlines in the content
                prompt = card["prompt"].replace("\t", " ").replace("\n", " ").strip()
                answer = card["answer"].replace("\t", " ").replace("\n", " ").strip()
                f.write(f"{prompt}\t{answer}\n")

        logger.info(f"Saved {len(note_card.cards)} cards to {note_card.output_path}")

    except OSError as e:
        logger.error(f"Failed to save cards to {note_card.output_path}: {e}")
        raise


def split_cards(content: str) -> List[Dict[str, str]]:
    """
    Parse AI response into individual flashcards.

    Args:
        content: Raw AI response content

    Returns:
        List of dictionaries with 'prompt' and 'answer' keys

    Raises:
        FlashcardParsingError: If parsing fails
    """
    try:
        # Clean up the content
        content = content.strip()

        # Find content between START and END markers
        start_match = re.search(r"<START>(.*?)<END>", content, re.DOTALL)
        if not start_match:
            # Fallback: try to find cards without markers
            logger.warning(
                "No START/END markers found, attempting to parse entire content"
            )
            card_content = content
        else:
            card_content = start_match.group(1)

        # Remove newlines and extra spaces
        card_content = re.sub(r"\s+", " ", card_content).strip()

        # Split by ANSWER-END to get individual cards
        card_parts = card_content.split("<ANSWER-END>")

        cards = []
        for card_part in card_parts:
            card_part = card_part.strip()
            if not card_part:
                continue

            # Split by PROMPT-END to separate question and answer
            if "<PROMPT-END>" not in card_part:
                logger.warning(f"Skipping malformed card: {card_part[:50]}...")
                continue

            try:
                prompt_part, answer_part = card_part.split("<PROMPT-END>", 1)
                prompt = prompt_part.strip()
                answer = answer_part.strip()

                if prompt and answer:
                    cards.append({"prompt": prompt, "answer": answer})
                else:
                    logger.warning("Skipping card with empty prompt or answer")

            except ValueError:
                logger.warning(f"Failed to parse card: {card_part[:50]}...")
                continue

        if not cards:
            raise FlashcardParsingError("No valid cards found in AI response")

        logger.debug(f"Parsed {len(cards)} cards from AI response")
        return cards

    except Exception as e:
        logger.error(f"Failed to parse flashcards: {e}")
        raise FlashcardParsingError(f"Failed to parse flashcards: {e}")


def generate_flashcards_for_note(
    note_card: NoteCard, model: str, prompt: str = DEFAULT_PROMPT, max_retries: int = 3
) -> None:
    """
    Generate flashcards for a single note using AI.

    Args:
        note_card: NoteCard to process
        model: AI model name (LiteLLM format)
        prompt: Custom prompt template
        max_retries: Maximum number of retry attempts

    Raises:
        FlashcardGenerationError: If generation fails after retries
    """
    if not note_card.note.strip():
        logger.warning(f"Empty note content for {note_card.input_path}")
        note_card.cards = []
        return

    messages = [{"role": "user", "content": prompt + note_card.note}]

    for attempt in range(max_retries):
        try:
            logger.debug(
                f"Generating cards for {note_card.input_path} (attempt {attempt + 1})"
            )

            response = completion(model=model, messages=messages)

            if not response.choices or not response.choices[0].message.content:
                raise FlashcardGenerationError("Empty response from AI model")

            content = str(response.choices[0].message.content)
            cards = split_cards(content)
            note_card.cards = cards

            logger.info(f"Generated {len(cards)} cards for {note_card.input_path.name}")
            return

        except Exception as e:
            logger.warning(
                f"Attempt {attempt + 1} failed for {note_card.input_path}: {e}"
            )
            if attempt == max_retries - 1:
                logger.error(
                    f"Failed to generate cards for {note_card.input_path} after {max_retries} attempts"
                )
                raise FlashcardGenerationError(f"Failed to generate cards: {e}")


def generate_and_write_cards(
    note_cards: List[NoteCard],
    model: str = "gemini/gemini-2.0-flash-lite",
    prompt: Optional[str] = None,
    max_retries: int = 3,
) -> None:
    """
    Generate flashcards for multiple notes and save them.

    Args:
        note_cards: List of NoteCard objects to process
        model: AI model name (LiteLLM format)
        prompt: Custom prompt template (uses default if None)
        max_retries: Maximum retry attempts per note
    """
    if not note_cards:
        logger.info("No notes to process")
        return

    if prompt is None:
        prompt = DEFAULT_PROMPT

    successful = 0
    failed = 0

    with Progress(
        TextColumn("[bold blue]Processing:"),
        TextColumn("{task.fields[filename]}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("cards", total=len(note_cards), filename="")

        for nc in note_cards:
            try:
                # Update filename in progress bar
                progress.update(task, filename=nc.input_path.name)

                # Generate flashcards
                generate_flashcards_for_note(nc, model, prompt, max_retries)

                # Save to file
                save_as_anki(nc)
                successful += 1

            except Exception as e:
                logger.error(f"Failed to process {nc.input_path}: {e}")
                failed += 1

            finally:
                progress.advance(task)

    logger.info(f"Processing complete: {successful} successful, {failed} failed")
