from litellm import completion
from anknote.io.card import NoteCard
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
)

PROMPT = """You are generating Anki flashcards for a user to retain knowledge from their knowledge base. The user text will be a part of their knowledge base notes, and you need to take key concepts and questions for them to remember. Be selective and only take important information. Be concise and clear.
    Instructions to create a deck of flashcards:
    - Create a list of flash cards.
    - Keep the flashcards simple, clear, and focused on the most important information.
    - Use simple and direct language to make the cards easy to read and understand.
    - don't include obvious knowledge or irrelevant formulas. Focus on recalling conceptual links or ideas, and put in [] random comments from the notes that seem to enhance the flashcard idea, so that I can see more info when I do my flashcards
    - Focus on intuitions and non trivial ideas rather than just facts or simple definitions. this is important.
    - Directly write all the cards without repeating the initial text/note.
    - Only write the prompt (questions) and the answers, nothing else.
    - the list of cards should start with <START> and end with <END>.
    - Don't put any line breaks (\n) in the questions or the answers.

    The format of a single flashcard is something like this example `What is a GPU? <PROMPT-END> It is a computing unit dedicated to tensors and .. <ANSWER-END>` for each new line.

    Actual user's text you have to transform:
    """


def save_as_anki(note_card: NoteCard):
    assert note_card
    note_card.output_path.parent.mkdir(parents=True, exist_ok=True)
    with note_card.output_path.open("w", encoding="utf-8") as f:
        for card in note_card.cards:
            f.write(f"{card['prompt']}\t{card['answer']}\n")


def split_cards(content: str) -> list[dict[str, str]]:
    # Model output format
    # `prompt<PROMPT-END> answer<ANSWER-END>`
    content = content.replace("\n", "")
    content = content.split("<START>")[1]
    content = content.split("<END>")[0]
    cards = content.split("<ANSWER-END>")

    return [
        {
            "prompt": card.split("<PROMPT-END>")[0].strip(),
            "answer": card.split("<PROMPT-END>")[1].strip(),
        }
        for card in cards
        if card
    ]


def generate_and_write_cards(
    note_cards: list,
    model: str = "gemini/gemini-2.0-flash-lite",
) -> None:
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
            messages = [{"content": PROMPT + nc.note}]
            response = str(
                completion(model=model, messages=messages).choices[0].message.content
            )

            cards = split_cards(response)
            nc.cards = cards

            # Update filename in progress bar
            progress.update(task, filename=nc.input_path.name)
            save_as_anki(nc)

            progress.advance(task)
