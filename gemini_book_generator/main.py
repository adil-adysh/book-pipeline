import os
import tempfile
import argparse
from common_logger import logger
from helpers import load_prompt, get_prompt_file_path
from epub_generator import create_epub_from_md
from book_pipeline import generate_book_pipeline


def parse_cli_args():
    """Parse command-line arguments for optional inputs."""
    parser = argparse.ArgumentParser(
        description="Generate an EPUB book from prompts and subtopics.",
        add_help=False,  # Disable default help to add a custom help flag.
    )
    # Custom help flag: When provided, shows usage info and exits immediately.
    parser.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    parser.add_argument(
        "-s",
        "--subtopics-list",
        help="Comma-separated list of subtopics to include (optional).",
        default="",
    )
    parser.add_argument(
        "-t",
        "--toc-prompt-file",
        help="Path to a custom Table of Contents prompt file (optional).",
        default="",
    )
    parser.add_argument(
        "-c",
        "--chapter-prompt-file",
        help="Path to a custom chapter prompt file (optional).",
        default="",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose logging.",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available Gemini models and exit.",
    )
    args, _ = parser.parse_known_args()
    return args


def get_api_key():
    """Retrieve and validate the API key from the environment."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return gemini_api_key


def main():
    try:
        # Validate that the API key exists.
        get_api_key()

        # Parse CLI args early so that --help is processed before any interactive input.
        args = parse_cli_args()

        # New: If --list-models flag provided, list models and exit.
        if args.list_models:
            from gemini_book_generator.gemini_llm import GeminiLLM

            models = GeminiLLM.list_models()
            print("Available Gemini models:")
            for model in models:
                print(f"- {model}")
            return

        # Use common logger with debug flag if needed.
        if args.debug:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        # Now, gather mandatory inputs as strings.
        topic = input("Enter the topic for the book: ").strip()
        chapter_count = input("Enter the number of chapters to generate: ").strip()

        # Load primary prompt templates.
        toc_prompt_text = load_prompt(get_prompt_file_path("toc_prompt.txt"))
        chapter_prompt_text = load_prompt(get_prompt_file_path("chapter_prompt.txt"))
        logger.debug("Initial ToC prompt text: %s", toc_prompt_text)
        logger.debug("Initial chapter prompt text: %s", chapter_prompt_text)

        # Get current working directory to resolve secondary prompt file paths.
        cur_dir = os.getcwd()

        # Append secondary ToC prompt details if provided.
        if args.toc_prompt_file:
            try:
                toc_prompt_path = args.toc_prompt_file
                # If not an absolute path, join with the current directory.
                if not os.path.isabs(toc_prompt_path):
                    toc_prompt_path = os.path.join(cur_dir, toc_prompt_path)
                secondary_toc_prompt = load_prompt(toc_prompt_path)
                toc_prompt_text += "\n" + secondary_toc_prompt
                logger.debug("Appended secondary ToC prompt: %s", secondary_toc_prompt)
            except Exception as e:
                logger.warning("Could not load ToC prompt file: %s", e)

        # Append secondary chapter prompt details if provided.
        if args.chapter_prompt_file:
            try:
                chapter_prompt_path = args.chapter_prompt_file
                # If not an absolute path, join with the current directory.
                if not os.path.isabs(chapter_prompt_path):
                    chapter_prompt_path = os.path.join(cur_dir, chapter_prompt_path)
                secondary_chapter_prompt = load_prompt(chapter_prompt_path)
                chapter_prompt_text += "\n" + secondary_chapter_prompt
                logger.debug(
                    "Appended secondary chapter prompt: %s", secondary_chapter_prompt
                )
            except Exception as e:
                logger.warning("Could not load chapter prompt file: %s", e)

        epub_filename = f"{topic}.epub"
        book_title = f"Book on {topic}"

        # Use a temporary directory for Markdown files.
        with tempfile.TemporaryDirectory() as temp_dir:
            generate_book_pipeline(
                topic=topic,
                chapter_count=chapter_count,  # Chapter count remains a string.
                directory=temp_dir,
                sub_topics=args.subtopics_list,  # Subtopics remain as a string.
                chapter_prompt_text=chapter_prompt_text,
                toc_prompt_text=toc_prompt_text,
            )
            create_epub_from_md(epub_filename, book_title, directory=temp_dir)

        logger.info("Temporary files cleaned up. EPUB saved as '%s'.", epub_filename)
    except Exception as e:
        logger.error("Error: %s", e)


if __name__ == "__main__":
    main()
