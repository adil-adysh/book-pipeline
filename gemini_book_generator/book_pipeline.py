import os
import json
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List
from gemini_llm import GeminiLLM


# --- Pydantic Models for ToC ---
class SectionModel(BaseModel):
    number: str
    title: str
    subsections: List['SectionModel'] = []

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

SectionModel.update_forward_refs()

class ToC(BaseModel):
    chapters: List[SectionModel]


def generate_book_pipeline(
    topic: str,
    chapter_count: str,
    directory: str,
    sub_topics: str,
    chapter_prompt_text: str,
    toc_prompt_text: str,
):
    # DEPRECATED: This pipeline has been replaced by the LangGraph-based pipeline in book_graph.py.
    # Please use book_graph.py for all future book generation workflows.
    # The code below is retained for reference only and will not be maintained.


def traverse_sections(sections, generated_prompts_dir, chapter_prompt_template):
    prompt_paths = []
    for section in sections:
        safe_section_number = section.number.replace('.', '_')
        prompt_filename = f"section_{safe_section_number}_prompt.txt"
        prompt_path = os.path.join(generated_prompts_dir, prompt_filename)
        # Build a summary of immediate subsections
        subsection_summary = ""
        if hasattr(section, 'subsections') and section.subsections:
            subsection_summary = "\nSubsections:\n" + "\n".join([
                f"- {sub.number}: {sub.title}" for sub in section.subsections
            ]) + "\n"
        # Always write (or overwrite) the prompt template for review
        with open(prompt_path, "w", encoding="utf-8") as pf:
            pf.write(f"# Prompt template for {section.number}. {section.title}\n\n")
            pf.write(subsection_summary)
            pf.write(chapter_prompt_template.replace("{chapter}", f"{section.number}. {section.title}"))
        prompt_paths.append(prompt_path)
        # Recursively process subsections
        if hasattr(section, 'subsections') and section.subsections:
            prompt_paths.extend(traverse_sections(section.subsections, generated_prompts_dir, chapter_prompt_template))
    return prompt_paths
