from pathlib import Path

PROMPT = """You are generating Anki flashcards for a user to retain knowledge from their knowledge base. The user text will be a part of their knowledge base notes, and you need to take key concepts and questions for them to remember. Be selective and only take important information. Be concise and clear.
    Instructions to create a deck of flashcards:
    - Keep the flashcards simple, clear, and focused on the most important information.
    - Use simple and direct language to make the cards easy to read and understand.
    - don't include obvious knowledge or irrelevant formulas. Focus on recalling conceptual links or ideas, and put in [] random comments from the notes that seem to enhance the flashcard idea, so that I can see more info when I do my flashcards
    - Focus on intuitions and non trivial ideas rather than just facts or simple definitions. this is important.
    Example text:
        notion of work: how much effort had to be given what we know about the configuration, to create it
        for electrostatics, this means taking every pair of units of charge and considering how much the electrostatic force pushes back against them being where they are, from infinity
        +- force along path from infinity
        want to develop better intuition on the relationship between work and energy #todo
        electric potential of a charge can be viewed as how the introduction of the charge changes the total work needed to create the system
        Total Energy = PE + KE
        can obtain the same with unit energy density of e0 / 2 * |E|^2
        being curl free amounts to being 0 around closed loop, how does this relate to the intuition of curl as measuring rotation, and allows us to create potential, #todo
        mechanism/framing of electric potential gives us a simpler primitiive to get the E-field and study other prpoperties of the electric config with
        in conducting materials charge elements move freely and will rearrange to minimize PE
            think more about this minimization principle #todo
            linked to work: the charges slide naturally towards low-energy minima
        Earnshaw's theorem: it's impossible to build a stable config w/ only coulomb forces #todo ask about this
        uniqueness theorem:
            fixing the E-field or net charge on each conductor for a set of conductors is enough to determine E-field uniquely
    The format of the flashcards is `prompt; "answer"` for each new line.
    Flashcards (keep in mind format):
    work in E&M; "How much effort to create a given configuration, in electrostatics, this means taking into account repulsive forces
    electric potential of a charge; "how much introduction of charge changes total work needed to create system"
    curl free; "being 0 around closed loop, [relate to intuition of curl as measuring rotation]"
    why do we use electric potential rather than E-field; "simpler primitive to get E-field and study other properties of electric config with"
    minimization principle in conducting materials; "charges slide naturally towards low-energy minima, creating elegant and useful properties"
    Earnshaw's theorem; "impossible to build a stable config w/ only coulomb forces"
    Actual text:
    """


def write_cards(
    note_cards: list,
    output_path: Path,
    model: str = "gemini/gemini-2.0-flash-lite",
) -> None:
    from litellm import completion

    messages = [{"content": PROMPT + note_cards[0].note}]
    response = completion(model=model, messages=messages)

    print(f"\n\n\n{response=}\n\n\n")
