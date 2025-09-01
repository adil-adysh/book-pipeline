import os
import json
from langgraph.graph import StateGraph
from langchain_core.prompts import PromptTemplate
from gemini_llm import GeminiLLM
import argparse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# --- State Model ---
class StateModel(BaseModel):
    topic: str
    chapter_count: str
    output_dir: str
    # sub_topics removed
    chapter_prompt_text: str
    toc_prompt_text: str
    repo_root: str
    toc_dict: Optional[Dict[str, Any]] = None
    toc_json_path: Optional[str] = None

# --- Node: Generate ToC ---
def generate_toc_node(state):
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
    )
    toc_template = PromptTemplate(
        input_variables=["topic", "chapterCount", "subTopics"],
        template=state.toc_prompt_text,
    )
    toc_chain = toc_template | gemini_llm
    toc_raw = toc_chain.invoke({
        "topic": state.topic,
        "chapterCount": state.chapter_count,
        "subTopics": "",
    })
    toc_text = toc_raw
    if toc_text.startswith("```json"):
        toc_text = toc_text.replace("```json", "", 1)
    if toc_text.endswith("```"):
        toc_text = toc_text.rsplit("```", 1)[0]
    toc_text = toc_text.strip()
    toc_dict = json.loads(toc_text)
    state.toc_dict = toc_dict
    return state

# --- Node: Write ToC JSON ---
def write_toc_node(state):
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    toc_json_path = os.path.join(generated_prompts_dir, "book_index.json")
    with open(toc_json_path, "w", encoding="utf-8") as f:
        json.dump(state.toc_dict, f, indent=2)
    state.toc_json_path = toc_json_path
    return state

# --- Node: Pause for ToC review ---
def review_toc_node(state):
    input(f"Review and edit the generated Table of Contents in '{state.toc_json_path}' (located in 'generated-prompts'). Press Enter to continue...")
    # Always re-read the file after user edit
    with open(state.toc_json_path, "r", encoding="utf-8") as f:
        state.toc_dict = json.load(f)
    return state

# --- Node: Generate prompt templates for all sections ---
def write_prompts_node(state):
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    section_prompt_path = os.path.join(state.repo_root, "gemini_book_generator", "prompts", "section_prompt.txt")
    def traverse_sections(sections, book_title, chapter_title, chapter_summary, section_prompt_template):
        prompt_paths = []
        for section in sections:
            safe_section_number = section["number"].replace('.', '_')
            prompt_filename = f"section_{safe_section_number}_prompt.txt"
            prompt_path = os.path.join(generated_prompts_dir, prompt_filename)
            subsection_summary = ""
            if "subsections" in section and section["subsections"]:
                subsection_summary = "\nSubsections:\n" + "\n".join([
                    f"- {sub['number']}: {sub['title']}" for sub in section["subsections"]
                ]) + "\n"
            prompt_vars = {
                "book_title": book_title,
                "chapter_title": chapter_title,
                "chapter_summary": chapter_summary,
                "section_title": section["title"],
                "section_number": section["number"],
            }
            with open(prompt_path, "w", encoding="utf-8") as pf:
                pf.write(f"# Prompt template for {section['number']}. {section['title']}\n\n")
                pf.write(subsection_summary)
                pf.write(section_prompt_template.format(**prompt_vars))
            prompt_paths.append(prompt_path)
            if "subsections" in section and section["subsections"]:
                prompt_paths.extend(traverse_sections(section["subsections"], book_title, chapter_title, chapter_summary, section_prompt_template))
        return prompt_paths

    # Generate intermediary chapter prompt files for each chapter
    chapter_prompt_path_template = os.path.join(generated_prompts_dir, "chapter_{chapter_number}_prompt.txt")
    chapter_prompt_template_path = os.path.join(state.repo_root, "gemini_book_generator", "prompts", "chapter_prompt.txt")
    with open(chapter_prompt_template_path, "r", encoding="utf-8") as f:
        chapter_prompt_template = f.read()
    with open(section_prompt_path, "r", encoding="utf-8") as f:
        section_prompt_template = f.read()

    book_title = state.topic
    chapters = state.toc_dict["chapters"]
    for chapter in chapters:
        chapter_title = chapter["title"]
        chapter_summary = chapter.get("summary", "")
        chapter_number = chapter["number"] if "number" in chapter else ""
        chapter_vars = {
            "book_title": book_title,
            "book_summary": "",  # Can be filled from state or ToC if available
            "subtopics": "",      # Can be filled from state if available
            "chapter_title": chapter_title,
            "chapter_number": chapter_number,
            "previous_chapter_summary": "",  # Can be filled if available
        }
        chapter_prompt_path = chapter_prompt_path_template.format(chapter_number=chapter_number.replace('.', '_'))
        with open(chapter_prompt_path, "w", encoding="utf-8") as pf:
            pf.write(f"# Prompt template for chapter {chapter_number}: {chapter_title}\n\n")
            pf.write(chapter_prompt_template.format(**chapter_vars))
        traverse_sections(chapter.get("subsections", [chapter]), book_title, chapter_title, chapter_summary, section_prompt_template)
    return state
    with open(section_prompt_path, "r", encoding="utf-8") as f:
        section_prompt_template = f.read()
    book_title = state.topic
    chapters = state.toc_dict["chapters"]
    for chapter in chapters:
        chapter_title = chapter["title"]
        chapter_summary = chapter.get("summary", "")
        traverse_sections(chapter.get("subsections", [chapter]), book_title, chapter_title, chapter_summary, section_prompt_template)
    return state

# --- Node: Pause for prompt review ---
def review_prompts_node(state):
    input("Review and edit the generated section and chapter prompt templates in 'generated-prompts/'. Press Enter to continue...")
    # No direct state update needed here, as prompts are re-read in generate_content_node
    return state

# --- Node: Generate content for all sections ---
def generate_content_node(state):
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    section_prompt_path = os.path.join(state.repo_root, "gemini_book_generator", "prompts", "section_prompt.txt")
    def get_chapter_prompt_path(chapter_number: str) -> str:
        safe_chapter_number = chapter_number.replace('.', '_')
        return os.path.join(generated_prompts_dir, f"chapter_{safe_chapter_number}_prompt.txt")

    def pad_section_number(section_number: str, width: int = 3) -> str:
        parts = section_number.split('.')
        return '_'.join([str(part).zfill(width) for part in parts])

    def traverse_content(sections, gemini_llm, directory, section_prompt_template, book_title, chapter_title, chapter_summary):
        for section in sections:
            safe_section_number = pad_section_number(section["number"])
            section_heading = f"{section['number']}. {section['title']}"
            print(f"\nGenerating content for section: {section_heading}")
            prompt_vars = {
                "book_title": book_title,
                "chapter_title": chapter_title,
                "chapter_summary": chapter_summary,
                "section_title": section["title"],
                "section_number": section["number"],
            }
            section_template = PromptTemplate(
                input_variables=list(prompt_vars.keys()),
                template=section_prompt_template
            )
            section_chain = section_template | gemini_llm
            section_raw = section_chain.invoke(prompt_vars)
            if isinstance(section_raw, dict) and "text" in section_raw:
                section_content = section_raw["text"]
            elif isinstance(section_raw, str):
                section_content = section_raw
            else:
                print(f"Unexpected section format for {section_heading}: {section_raw}")
                continue
            markdown_filename = f"section_{safe_section_number}.md"
            section_md_path = os.path.join(directory, markdown_filename)
            base_path = section_md_path
            suffix = 1
            while os.path.exists(section_md_path):
                section_md_path = base_path.replace('.md', f'_{suffix}.md')
                suffix += 1
            with open(section_md_path, "w", encoding="utf-8") as f:
                f.write(f"# {section_heading}\n\n")
                f.write(section_content)
            print(f"Saved {section_md_path}")
            if "subsections" in section and section["subsections"]:
                traverse_content(
                    section["subsections"],
                    gemini_llm,
                    directory,
                    section_prompt_template,
                    book_title,
                    chapter_title,
                    chapter_summary,
                )

    def generate_chapter(chapter, gemini_llm, output_dir, chapter_prompt_template, book_title, book_summary, subtopics, previous_chapter_summary):
        chapter_vars = {
            "book_title": book_title,
            "book_summary": book_summary,
            "subtopics": subtopics,
            "chapter_title": chapter["title"],
            "chapter_number": chapter["number"] if "number" in chapter else "",
            "previous_chapter_summary": previous_chapter_summary,
        }
        chapter_template = PromptTemplate(
            input_variables=list(chapter_vars.keys()),
            template=chapter_prompt_template
        )
        chapter_chain = chapter_template | gemini_llm
        chapter_raw = chapter_chain.invoke(chapter_vars)
        chapter_content = chapter_raw["text"] if isinstance(chapter_raw, dict) and "text" in chapter_raw else chapter_raw
        markdown_filename = f"chapter_{chapter_vars['chapter_number'].zfill(3)}.md" if chapter_vars["chapter_number"] else f"chapter_{chapter_vars['chapter_title'].replace(' ', '_')}.md"
        chapter_md_path = os.path.join(output_dir, markdown_filename)
        with open(chapter_md_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_vars['chapter_title']}\n\n")
            f.write(chapter_content)
        print(f"Saved {chapter_md_path}")
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
    )
    with open(section_prompt_path, "r", encoding="utf-8") as f:
        section_prompt_template = f.read()
    book_title = state.topic
    book_summary = ""  # You can populate this from state or ToC if available
    subtopics = getattr(state, 'sub_topics', "")
    chapters = state.toc_dict["chapters"]
    previous_chapter_summary = ""
    for chapter in chapters:
        chapter_number = chapter["number"] if "number" in chapter else ""
        chapter_prompt_path = get_chapter_prompt_path(chapter_number)
        with open(chapter_prompt_path, "r", encoding="utf-8") as f:
            chapter_prompt_template = f.read()
        # Generate chapter content with context
        generate_chapter(
            chapter,
            gemini_llm,
            state.output_dir,
            chapter_prompt_template,
            book_title,
            book_summary,
            subtopics,
            previous_chapter_summary,
        )
        chapter_title = chapter["title"]
        chapter_summary = chapter.get("summary", "")
        previous_chapter_summary = chapter_summary
        traverse_content(
            [chapter],
            gemini_llm,
            state.output_dir,
            section_prompt_template,
            book_title,
            chapter_title,
            chapter_summary,
        )
    return state

# --- Node: End ---
def end_node(state):
    print("Book generation complete.")
    return state

# --- Build LangGraph ---
def build_book_graph():
    graph = StateGraph(StateModel)
    graph.add_node("generate_toc", generate_toc_node)
    graph.add_node("write_toc", write_toc_node)
    graph.add_node("review_toc", review_toc_node)
    graph.add_node("write_prompts", write_prompts_node)
    graph.add_node("review_prompts", review_prompts_node)
    graph.add_node("generate_content", generate_content_node)
    graph.add_node("end", end_node)
    graph.add_edge("generate_toc", "write_toc")
    graph.add_edge("write_toc", "review_toc")
    graph.add_edge("review_toc", "write_prompts")
    graph.add_edge("write_prompts", "review_prompts")
    graph.add_edge("review_prompts", "generate_content")
    graph.add_edge("generate_content", "end")
    graph.set_entry_point("generate_toc")
    return graph

# --- Entrypoint ---
def run_book_graph(topic, chapter_count, output_dir, chapter_prompt_text, toc_prompt_text):
    repo_root = os.path.dirname(os.path.dirname(__file__))
    state = {
        "topic": topic,
        "chapter_count": chapter_count,
        "output_dir": output_dir,
        "chapter_prompt_text": chapter_prompt_text,
        "toc_prompt_text": toc_prompt_text,
        "repo_root": repo_root,
    }
    graph = build_book_graph()
    compiled_graph = graph.compile()
    compiled_graph.invoke(state)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Gemini Book Generator with LangGraph")
    parser.add_argument("--topic", required=True, help="Book topic")
    parser.add_argument("--chapter-count", required=True, help="Number of chapters")
    parser.add_argument("--output-dir", required=True, help="Output directory for markdown files")
    # --subtopics removed
    parser.add_argument("--chapter-prompt-file", required=True, help="Path to chapter prompt template file")
    parser.add_argument("--toc-prompt-file", required=True, help="Path to ToC prompt template file")
    args = parser.parse_args()
    with open(args.chapter_prompt_file, "r", encoding="utf-8") as f:
        chapter_prompt_text = f.read()
    with open(args.toc_prompt_file, "r", encoding="utf-8") as f:
        toc_prompt_text = f.read()
    run_book_graph(
        topic=args.topic,
        chapter_count=args.chapter_count,
        output_dir=args.output_dir,
        chapter_prompt_text=chapter_prompt_text,
        toc_prompt_text=toc_prompt_text,
    )
