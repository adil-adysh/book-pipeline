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

    # Save the actual generated ToC (JSON) to prompts/generated/book_index.json
    generated_prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "generated")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    toc_json_path = os.path.join(generated_prompts_dir, "book_index.json")
    with open(toc_json_path, "w", encoding="utf-8") as f:
        json.dump(toc_dict, f, indent=2)
    print(f"Saved ToC JSON to {toc_json_path}")

    # Pause for user review/edit of ToC JSON
    input("Review and edit the generated Table of Contents in 'prompts/generated/book_index.json'. Press Enter to continue...")

    # Validate and load ToC after user review
    try:
        with open(toc_json_path, "r", encoding="utf-8") as f:
            toc_dict = json.load(f)
        toc_data = ToC(**toc_dict)
        print("Validated ToC. Proceeding with chapter generation.")
    except Exception as e:
        print(f"Error validating ToC: {e}")
        return

    # ----- Step 1b: Generate per-section prompt template files -----
    chapter_prompt_template = chapter_prompt_text.strip()
    print(f"Generating prompt templates for all sections/subsections in {generated_prompts_dir}")
    all_prompt_paths = traverse_sections(toc_data.chapters, generated_prompts_dir, chapter_prompt_template)
    print(f"All section prompt templates written. Review/edit them before continuing.")
    input("Review and edit the generated section prompt templates in 'prompts/generated/'. Press Enter to continue...")

    # ----- Step 2: Generate Detailed Content for Each Section (from updated ToC) -----
    def generate_content_for_sections(sections, generated_prompts_dir, gemini_llm, directory):
        for section in sections:
            safe_section_number = section.number.replace('.', '_')
            prompt_filename = f"section_{safe_section_number}_prompt.txt"
            prompt_path = os.path.join(generated_prompts_dir, prompt_filename)
            # Read the (possibly edited/custom) prompt template for this section
            with open(prompt_path, "r", encoding="utf-8") as pf:
                section_prompt = pf.read()
            section_template = PromptTemplate(
                input_variables=["chapter"],
                template=section_prompt,
            )
            section_chain = section_template | gemini_llm
            section_heading = f"{section.number}. {section.title}"
            print(f"\nGenerating content for section: {section_heading}")
            section_raw = section_chain.invoke({"chapter": section_heading})
            print(f"Raw content for {section_heading}:", section_raw)
            if isinstance(section_raw, dict) and "text" in section_raw:
                section_content = section_raw["text"]
            elif isinstance(section_raw, str):
                section_content = section_raw
            else:
                print(f"Unexpected section format for {section_heading}: {section_raw}")
                continue
            markdown_filename = f"section_{safe_section_number}.md"
            section_md_path = os.path.join(directory, markdown_filename)
            with open(section_md_path, "w", encoding="utf-8") as f:
                f.write(f"# {section_heading}\n\n")
                f.write(section_content)
            print(f"Saved {section_md_path}")
            # Recursively process subsections
            if hasattr(section, 'subsections') and section.subsections:
                generate_content_for_sections(section.subsections, generated_prompts_dir, gemini_llm, directory)

    generate_content_for_sections(toc_data.chapters, generated_prompts_dir, gemini_llm, directory)


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
