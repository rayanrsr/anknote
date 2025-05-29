# Anknote

## Project Goal

The goal of this project is to [TODO: Describe the project goal here].

## Support

If you need help or have any questions, please [TODO: Describe how to get support, e.g., open an issue, contact email].
=======
# Anknote 📝✨

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/your_username/anknote/actions) <!-- TODO: Replace with actual
build status badge -->

**Anknote is a powerful command-line tool that intelligently generates Anki flashcards from your markdown notes using state-of-the-art AI models.**

Stop manually creating flashcards and let Anknote help you focus on what truly matters: learning and retaining knowledge efficiently.

## Overview

Anknote processes your markdown files (either a single file or an entire directory structure) and leverages AI to identify key concepts, important
information, and insightful questions. It then transforms these into a structured format ready for import into Anki, your favorite spaced repetition
software.

The tool is designed to create flashcards that emphasize understanding and intuition rather than rote memorization of simple facts or definitions.

## Features

*   **AI-Powered Card Generation:** Uses language models via LiteLLM (e.g., Gemini, GPT) to create high-quality flashcards.
*   **Markdown Input:** Accepts individual `.md` files or recursively scans directories for notes.
*   **Anki-Compatible Output:** Generates `.tsv` files that can be directly imported into Anki.
*   **Customizable AI Model:** Easily switch between different AI models supported by LiteLLM.
*   **Selective Processing:** Avoids re-processing notes for which flashcards already exist (unless forced).
*   **In-Place Output:** Option to save generated flashcards alongside your original notes.
*   **Progress Tracking:** Clear progress bar during the generation process.
*   **Focus on Conceptual Understanding:** Prompts are designed to extract non-trivial ideas and conceptual links.

## How It Works

1.  **Input:** You provide a path to a markdown file or a directory containing markdown files.
2.  **Parsing & Retrieval:** Anknote reads your notes. If a directory is provided, it recursively finds all `.md` files.
3.  **AI Processing:** For each note, the content is sent to the configured AI model with a specialized prompt. This prompt guides the AI to extract key
information and formulate question/answer pairs suitable for flashcards.
4.  **Formatting:** The AI's response is parsed into a list of distinct flashcards.
5.  **Output:** The generated flashcards are saved as `.tsv` files (tab-separated values), with each line representing a card (prompt and answer). The
output directory structure mirrors the input structure.

## Installation

```bash
# TODO: Add installation instructions once packaging is set up
# For example, if published on PyPI:
# pip install anknote


Ensure you have Python 3.x installed. Dependencies are listed in pyproject.toml.


Usage

The primary way to use Anknote is through its command-line interface.


anknote <input_path> [options]


Arguments:

 • input_path: (Required) Path to the input markdown file or directory of markdown files.

Options:

 • -o, --output <path>: Specifies the directory where generated Anki cards (.tsv files) will be stored. Defaults to the current directory (.).
 • -m, --model <model_name>: Sets the AI model to use for card generation, following the LiteLLM format (e.g., gemini/gemini-2.0-flash-lite, gpt-4o).
   Defaults to gemini/gemini-2.0-flash-lite.
 • -f, --force-overwrite: Re-generates flashcards for all input files, even if corresponding output files already exist.
 • -i, --in-place: Saves the output .tsv files in the same directory as their corresponding input .md files. This overrides the --output option.
 • --help: Shows the help message and exits.

Examples:

 1 Generate cards from a single note file:

   anknote my_notes/important_topic.md

   (This will create important_topic.tsv in the current directory)
 2 Generate cards from an entire directory of notes and save them to a specific output folder:

   anknote ./my_knowledge_base -o ./anki_cards

 3 Generate cards using a different AI model (e.g., GPT-4o):

   anknote my_notes/chapter1.md -m gpt-4o

 4 Force overwrite existing cards for a directory:

   anknote ./my_notes -f

 5 Generate cards in-place (next to original markdown files):

   anknote ./my_notes -i



Configuration

AI Model API Keys:

Anknote uses LiteLLM to interact with various AI models. You will typically need to set environment variables for the API keys of the models you intend to
use. For example:

 • For OpenAI models: OPENAI_API_KEY="your_api_key"
 • For Google Gemini models: GEMINI_API_KEY="your_api_key"

Please refer to the LiteLLM documentation for specific instructions on configuring API keys for different providers.


Contributing

Contributions are welcome! If you'd like to contribute, please:

 1 Fork the repository.
 2 Create a new branch for your feature or bug fix.
 3 Make your changes.
 4 Add tests for your changes.
 5 Ensure all tests pass.
 6 Submit a pull request.

Please open an issue first to discuss any significant changes.


License

This project is licensed under the terms of the LICENSE file.


Support


If you encounter any issues, have questions, or want to suggest features, please open an issue on GitHub.
