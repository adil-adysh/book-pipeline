import os
import json
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List
from gemini_llm import GeminiLLM


# --- Pydantic Models for ToC ---
class ChapterModel(BaseModel):
    number: str
    title: str


class ToC(BaseModel):
    chapters: List[ChapterModel]


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
    # Chain the prompt and the LLM using the new RunnableSequence style.
    toc_chain = toc_template | gemini_llm

    # Generate ToC using the new invoke() approach
    toc_raw = toc_chain.invoke(
        {
            "topic": topic,
            "chapterCount": chapter_count,
            "subTopics": sub_topics,
        }
    )

    # Debugging: Print raw ToC output
    print("Raw ToC output:", toc_raw)

    # Process the returned text: remove code block markers and parse JSON.
    toc_text = toc_raw
    if toc_text.startswith("```json"):
        toc_text = toc_text.replace("```json", "", 1)
    if toc_text.endswith("```"):
        toc_text = toc_text.rsplit("```", 1)[0]
    toc_text = toc_text.strip()

    try:
        toc_dict = json.loads(toc_text)
        toc_data = ToC(**toc_dict)
    except Exception as e:
        print(f"Error parsing ToC data: {e}")
        return

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
        input_variables=["chapter"],
        template=chapter_prompt_text,
    )
    chapter_chain = chapter_template | gemini_llm

    for chapter in toc_data.chapters:
        chapter_heading = f"{chapter.number}. {chapter.title}"
        print(f"\nGenerating content for chapter: {chapter_heading}")

        chapter_raw = chapter_chain.invoke({"chapter": chapter_heading})
        print(f"Raw content for {chapter_heading}:", chapter_raw)

        # Check if chapter_raw is a dict with 'text', otherwise treat it as a string.
        if isinstance(chapter_raw, dict) and "text" in chapter_raw:
            chapter_content = chapter_raw["text"]
        elif isinstance(chapter_raw, str):
            chapter_content = chapter_raw
        else:
            print(f"Unexpected chapter format for {chapter_heading}: {chapter_raw}")
            continue

        safe_chapter_number = chapter.number.replace(".", "_")
        markdown_filename = f"chapter_{safe_chapter_number}.md"
        chapter_md_path = os.path.join(directory, markdown_filename)
        with open(chapter_md_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_heading}\n\n")
            f.write(chapter_content)
        print(f"Saved {chapter_md_path}")
