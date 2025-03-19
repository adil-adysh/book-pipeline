import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List
from gemini_llm import GeminiLLM


# --- Pydantic Models for ToC ---
class ChapterModel(BaseModel):
    number: str
    title: str


class ToC(BaseModel):
    chapters: List[ChapterModel]


# --- Output Parser for Structured ToC ---
toc_parser = PydanticOutputParser(pydantic_object=ToC)


def generate_book_pipeline(
    topic: str,
    chapter_count: str,
    directory: str,
    sub_topics: str,
    chapter_prompt_text: str,
    toc_prompt_text: str,
):
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
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
