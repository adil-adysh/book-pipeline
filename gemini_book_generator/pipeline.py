import os
import time
import markdown
import tempfile
import argparse
from ebooklib import epub

from google import genai
from langchain.llms.base import LLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Any, Optional


# --- Helper to Load Prompts from Files ---
def load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# --- Pydantic Models for ToC ---
class ChapterModel(BaseModel):
    number: str
    title: str


class ToC(BaseModel):
    chapters: List[ChapterModel]


# --- Output Parser for Structured ToC ---
toc_parser = PydanticOutputParser(pydantic_object=ToC)


# --- Functions for EPUB Generation ---
def extract_chapter_key(filename: str):
    """
    Extract a tuple of integers from a filename.
    For example, 'chapter_1_2.md' returns (1, 2).
    """
    basename = os.path.splitext(filename)[0]
    if basename.startswith("chapter_"):
        num_part = basename[len("chapter_") :]
    else:
        return (-1,)
    try:
        return tuple(int(part) for part in num_part.split("_") if part)
    except ValueError:
        return (float("inf"),)


def get_sorted_chapter_files(directory="."):
    files = [
        f
        for f in os.listdir(directory)
        if f.startswith("chapter_") and f.endswith(".md")
    ]
    files.sort(key=extract_chapter_key)
    return files


def create_epub_from_md(epub_filename: str, book_title: str, directory="."):
    book = epub.EpubBook()
    book.set_title(book_title)
    book.set_language("en")

    spine = ["nav"]

    # Add the book index if it exists (assumed as preface/intro)
    index_path = os.path.join(directory, "book_index.md")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
        index_html = markdown.markdown(index_content)
        index_item = epub.EpubHtml(
            title="Table of Contents", file_name="index.xhtml", content=index_html
        )
        book.add_item(index_item)
        spine.append(index_item.file_name)

    # Process chapter Markdown files
    chapter_files = get_sorted_chapter_files(directory)
    for md_file in chapter_files:
        with open(os.path.join(directory, md_file), "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        chapter_title = os.path.splitext(md_file)[0]
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=md_file.replace(".md", ".xhtml"),
            content=html_content,
        )
        book.add_item(chapter)
        spine.append(chapter.file_name)

    book.toc = tuple(spine[1:])  # Skip the 'nav' element
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Optionally add CSS styling
    style = "body { font-family: Arial, sans-serif; }"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    book.spine = spine
    epub.write_epub(epub_filename, book, {})
    print(f"EPUB created: {epub_filename}")


# Retrieve your API key from environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")


# --- Custom LLM Wrapper for Gemini API ---
class GeminiLLM(LLM):
    api_key: str
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    client: genai.Client = genai.Client(api_key=gemini_api_key)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get("api_key")
        self.client = genai.Client(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _truncate_on_stop_tokens(self, text: str, stop: List[str]) -> str:
        for token in stop:
            if token in text:
                return text.split(token)[0]
        return text

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name, contents=prompt
                )
                if hasattr(response, "status_code") and response.status_code != 200:
                    raise RuntimeError(f"HTTP error: {response.status_code}")
                text = response.text.strip() if response.text else ""
                if stop:
                    text = self._truncate_on_stop_tokens(text, stop)
                return text
            except Exception as e:
                print(f"Attempt {attempt} failed with error: {e}")
                if attempt == max_retries:
                    raise RuntimeError(f"Failed after {max_retries} attempts: {str(e)}")
                time.sleep(2**attempt)
        raise RuntimeError("Unexpected error in _call method")


def generate_book_pipeline(
    topic: str,
    chapter_count: str,
    directory: str,
    sub_topics: str,
    chapter_prompt_text: str,
    toc_prompt_text: str,
):
    gemini_llm = GeminiLLM(
        api_key=gemini_api_key, model_name="gemini-2.0-flash", temperature=0.7
    )

    # ----- Step 1: Generate the Book Index (Table of Contents) -----
    toc_template = PromptTemplate(
        input_variables=["topic", "chapterCount", "subTopics"],
        template=toc_prompt_text,
    )
    toc_chain = LLMChain(llm=gemini_llm, prompt=toc_template, output_parser=toc_parser)
    toc_data = toc_chain.run(
        {
            "topic": topic,
            "chapterCount": chapter_count,
            "subTopics": sub_topics,
        }
    )
    print("Generated structured ToC:")
    print(toc_data)

    # Save the structured ToC to a Markdown file.
    toc_md_path = os.path.join(directory, "book_index.md")
    with open(toc_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Table of Contents for {topic}\n\n")
        for chapter in toc_data.chapters:
            f.write(f"{chapter.number}. {chapter.title}\n")
    print(f"Saved {toc_md_path}")

    # ----- Step 2: Generate Detailed Content for Each Chapter -----
    chapter_template = PromptTemplate(
        input_variables=["chapter"], template=chapter_prompt_text
    )
    chapter_chain = LLMChain(llm=gemini_llm, prompt=chapter_template)

    for chapter in toc_data.chapters:
        chapter_heading = f"{chapter.number}. {chapter.title}"
        print(f"\nGenerating content for chapter: {chapter_heading}")
        chapter_content = chapter_chain.run(chapter_heading)
        safe_chapter_number = chapter.number.replace(".", "_")
        markdown_filename = f"chapter_{safe_chapter_number}.md"
        chapter_md_path = os.path.join(directory, markdown_filename)
        with open(chapter_md_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_heading}\n\n")
            f.write(chapter_content)
        print(f"Saved {chapter_md_path}")


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
