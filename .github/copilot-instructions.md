# Copilot Instructions for Gemini Book Generator

## Project Overview
- **Gemini Book Generator** automates book creation using generative AI (Google Gemini API).
- Main logic is in `gemini_book_generator/` with entrypoint `main.py`.
- Books are generated from a topic, organized into chapters, and exported as EPUB files.
- Customization is supported via prompt files in `gemini_book_generator/prompts/`.

## Architecture & Key Components
- `book_pipeline.py`: Orchestrates the book generation workflow.
- `gemini_llm.py`: Handles communication with the Gemini API.
- `epub_generator.py`: Converts generated content into EPUB format.
- `common_logger.py`: Centralized logging for all modules.
- `helpers.py`: Utility functions for text and file operations.
- `prompts/`: Contains prompt templates for TOC and chapters.
- `gemini_config.json`: Stores configuration for Gemini API usage.

## Developer Workflows
- **Install dependencies:** `poetry install`
- **Activate environment:** `poetry shell`
- **Run generator:** `poetry run python gemini_book_generator/main.py`
- **Type checking:** `mypy gemini_book_generator/`
- **Custom prompts:** Pass `--toc-prompt-file` and `--chapter-prompt-file` to use custom templates.
- **API Key:** Set `GEMINI_API_KEY` in your environment before running.

## Patterns & Conventions
- All logging uses `common_logger.py` for consistency.
- Type hints are enforced; stubs in `stubs/` and `mypy.ini` for strict type checking.
- External API integration is abstracted in `gemini_llm.py`.
- Configuration is JSON-based (`gemini_config.json`).
- Command-line options are parsed in `main.py` (see `--help`).
- EPUB generation is isolated in `epub_generator.py` for easy format changes.

## Integration Points
- **Google Gemini API:** Requires valid API key; see `gemini_llm.py` for usage.
- **EPUB output:** Uses custom logic in `epub_generator.py`.
- **Type stubs:** Located in `stubs/` for external and internal modules.

## Example: Custom Book Generation
```pwsh
$env:GEMINI_API_KEY="your_api_key"
poetry run python gemini_book_generator/main.py --toc-prompt-file gemini_book_generator/prompts/toc_prompt.txt --chapter-prompt-file gemini_book_generator/prompts/chapter_prompt.txt --subtopics-list "AI,Machine Learning"
```

## Troubleshooting
- Check API key and dependencies if errors occur.
- Use `mypy` for type issues.
- Log output is in console via `common_logger.py`.

---

_Review and update this file as project structure or workflows change._
