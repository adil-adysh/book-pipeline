import os
import tempfile
import argparse
from helpers import load_prompt
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
        # Parse CLI args early so that --help is processed before any interactive input.
        args = parse_cli_args()

        # Validate that the API key exists.
        get_api_key()

        # Now, gather mandatory inputs as strings.
        topic = input("Enter the topic for the book: ").strip()
        chapter_count = input("Enter the number of chapters to generate: ").strip()

        # Load primary prompt templates.
        toc_prompt_text = load_prompt("toc_prompt.txt")
        chapter_prompt_text = load_prompt("chapter_prompt.txt")

        # Append secondary prompt details if provided.
        if args.toc_prompt_file:
            try:
                secondary_toc_prompt = load_prompt(args.toc_prompt_file)
                toc_prompt_text += "\n" + secondary_toc_prompt
            except Exception as e:
                print(f"Warning: Could not load ToC prompt file: {e}")

        if args.chapter_prompt_file:
            try:
                secondary_chapter_prompt = load_prompt(args.chapter_prompt_file)
                chapter_prompt_text += "\n" + secondary_chapter_prompt
            except Exception as e:
                print(f"Warning: Could not load chapter prompt file: {e}")

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

        print(f"Temporary files cleaned up. EPUB saved as '{epub_filename}'.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
