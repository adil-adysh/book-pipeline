import os
import tempfile
import argparse
from helpers import load_prompt
from epub_generator import create_epub_from_md
from book_pipeline import generate_book_pipeline

# Retrieve your API key from environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")


def main():
    # Mandatory inputs using input()
    topic = input("Enter the topic for the book: ")
    chapter_count = input("Enter number of chapters to be generated for the book: ")

    # Optional flags for subtopics and secondary prompt files
    parser = argparse.ArgumentParser(
        description="Optional flags for subtopics and secondary prompt file paths"
    )
    parser.add_argument(
        "--subtopics",
        help="Comma-separated list of subtopics (optional)",
        default="",
    )
    parser.add_argument(
        "--secondary-toc-prompt-file",
        help="Path to the secondary Table of Contents prompt file (optional)",
        default="",
    )
    parser.add_argument(
        "--secondary-chapter-prompt-file",
        help="Path to the secondary chapter prompt file (optional)",
        default="",
    )
    # Parse only known args so that it doesn't interfere with interactive inputs
    args, _ = parser.parse_known_args()

    # Load primary prompt templates from default files
    global toc_prompt_text, chapter_prompt_text
    toc_prompt_text = load_prompt("toc_prompt.txt")
    chapter_prompt_text = load_prompt("chapter_prompt.txt")

    # Append secondary prompt details if provided via flags
    if args.secondary_toc_prompt_file:
        try:
            secondary_toc_prompt = load_prompt(args.secondary_toc_prompt_file)
            toc_prompt_text += "\n" + secondary_toc_prompt
        except Exception as e:
            print(f"Warning: Could not load secondary ToC prompt file: {e}")
    if args.secondary_chapter_prompt_file:
        try:
            secondary_chapter_prompt = load_prompt(args.secondary_chapter_prompt_file)
            chapter_prompt_text += "\n" + secondary_chapter_prompt
        except Exception as e:
            print(f"Warning: Could not load secondary chapter prompt file: {e}")

    epub_filename = f"{topic}.epub"
    book_title = f"Book on {topic}"

    # Use a temporary directory to store Markdown files
    with tempfile.TemporaryDirectory() as temp_dir:
        generate_book_pipeline(
            topic=topic,
            chapter_count=chapter_count,
            directory=temp_dir,
            sub_topics=args.subtopics,
            chapter_prompt_text=chapter_prompt_text,
            toc_prompt_text=toc_prompt_text,
        )
        create_epub_from_md(epub_filename, book_title, directory=temp_dir)

    print(f"Temporary files cleaned up. EPUB saved as '{epub_filename}'.")


if __name__ == "__main__":
    main()
