import os
import json
from google import genai
from langchain.llms.base import LLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List


# --- Pydantic Models for ToC ---
class Chapter(BaseModel):
    number: str
    title: str


class ToC(BaseModel):
    chapters: List[Chapter]


# --- Output Parser for Structured ToC ---
toc_parser = PydanticOutputParser(pydantic_object=ToC)


# --- Helper to Load Prompts from Files Relative to This Script ---
def load_prompt(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# Load prompt templates from external files
toc_prompt_text = load_prompt("toc_prompt.txt")
chapter_prompt_text = load_prompt("chapter_prompt.txt")

# Retrieve your API key from an environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")


# --- Custom LLM Wrapper for Gemini API using google-genai ---
class GeminiLLM(LLM):
    api_key: str
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    client: any = None  # Holds the google-genai Client instance

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = genai.Client(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop=None) -> str:
        response = self.client.models.generate_content(
            model=self.model_name, contents=prompt
        )
        return response.text.strip()

    async def _acall(self, prompt: str, stop=None) -> str:
        raise NotImplementedError("Async call not implemented.")


# --- Pipeline Function ---
def generate_book_pipeline(topic: str):
    gemini_llm = GeminiLLM(
        api_key=gemini_api_key, model_name="gemini-2.0-flash", temperature=0.7
    )

    # ----- Step 1: Generate the Book Index (Table of Contents) -----
    toc_template = PromptTemplate(
        input_variables=["topic"],
        template=toc_prompt_text,
    )
    # Pass the output parser to the chain so the LLM output is automatically parsed.
    toc_chain = LLMChain(llm=gemini_llm, prompt=toc_template, output_parser=toc_parser)
    # Run the chain; toc_data is an instance of ToC.
    toc_data = toc_chain.run(topic)
    print("Generated structured ToC:")
    print(toc_data)

    # Save the structured ToC to a Markdown file.
    with open("book_index.md", "w", encoding="utf-8") as f:
        f.write(f"# Table of Contents for {topic}\n\n")
        for chapter in toc_data.chapters:
            f.write(f"{chapter.number}. {chapter.title}\n")
    print("Saved book_index.md")

    # ----- Step 2: Generate Detailed Content for Each Chapter -----
    chapter_template = PromptTemplate(
        input_variables=["chapter"], template=chapter_prompt_text
    )
    chapter_chain = LLMChain(llm=gemini_llm, prompt=chapter_template)

    for chapter in toc_data.chapters:
        chapter_heading = f"{chapter.number}. {chapter.title}"
        print(f"\nGenerating content for chapter: {chapter_heading}")
        chapter_content = chapter_chain.run(chapter_heading)
        # Replace dots with underscores in the chapter number for a safe filename.
        safe_chapter_number = chapter.number.replace(".", "_")
        markdown_filename = f"chapter_{safe_chapter_number}.md"
        with open(markdown_filename, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_heading}\n\n")
            f.write(chapter_content)
        print(f"Saved {markdown_filename}")


if __name__ == "__main__":
    topic = "Data Structures and Algorithms"
    topic = input("Enter the topic for the book: ")
    generate_book_pipeline(topic)
