# Gemini Book Generator

## Description

Gemini Book Generator is a LangChain-based pipeline that uses the Google Gen AI SDK to generate accessible book content for visually impaired users. The project automates converting markdown inputs into an EPUB book using customizable prompt templates and interactive inputs.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- A valid GEMINI_API_KEY environment variable set with your API key

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/adil-adysh/book-pipeline.git
    cd book-pipeline
    ```

2. Install project dependencies using Poetry:

    ```bash
    poetry install
    ```

### Usage

1. Set the GEMINI_API_KEY environment variable:

    ```bash
    # Linux/macOS
    export GEMINI_API_KEY=your_api_key

    # Windows
    set GEMINI_API_KEY=your_api_key
    ```

2. Run the main script:

    ```bash
    poetry run python gemini_book_generator/main.py
    ```

3. Follow the interactive prompts:
    - Enter the topic and number of chapters.
    - Optionally, provide paths for custom prompt files with:
        - `--toc-prompt-file` for the Table of Contents prompt.
        - `--chapter-prompt-file` for the chapter prompt.
        - `--subtopics-list` for a comma-separated list of subtopics.

4. The pipeline creates temporary markdown files and generates an EPUB file named after the provided topic.

### Examples

#### Without Flags

```bash
poetry run python gemini_book_generator/main.py
```

Follow the interactive prompts to enter the topic and number of chapters.

#### With Flags

```bash
poetry run python gemini_book_generator/main.py --toc-prompt-file path/to/toc_prompt.txt --chapter-prompt-file path/to/chapter_prompt.txt --subtopics-list "subtopic1,subtopic2,subtopic3"
```

### Getting Help

To get help on the available commands and options, use the `--help` flag:

```bash
poetry run python gemini_book_generator/main.py --help
```

### Troubleshooting

- Ensure all dependencies are installed via Poetry.
- Verify that the GEMINI_API_KEY environment variable is correctly set.
- Double-check custom prompt file paths provided via CLI flags.

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
