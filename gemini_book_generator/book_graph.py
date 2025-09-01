import os
import json
from langgraph.graph import StateGraph
from langchain_core.prompts import PromptTemplate
from gemini_llm import GeminiLLM
import argparse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# --- State Model ---
class StateModel(BaseModel):
    topic: str
    chapter_count: str
    output_dir: str
    sub_topics: Optional[str] = ""
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
        "subTopics": state.sub_topics,
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
    generated_prompts_dir = os.path.join(state.repo_root, "prompts", "generated")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    toc_json_path = os.path.join(generated_prompts_dir, "book_index.json")
    with open(toc_json_path, "w", encoding="utf-8") as f:
        json.dump(state.toc_dict, f, indent=2)
    state.toc_json_path = toc_json_path
    return state

# --- Node: Pause for ToC review ---
def review_toc_node(state):
    input(f"Review and edit the generated Table of Contents in '{state.toc_json_path}'. Press Enter to continue...")
    with open(state.toc_json_path, "r", encoding="utf-8") as f:
        state.toc_dict = json.load(f)
    return state

# --- Node: Generate prompt templates for all sections ---
def write_prompts_node(state):
    def traverse_sections(sections, generated_prompts_dir, chapter_prompt_template):
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
            with open(prompt_path, "w", encoding="utf-8") as pf:
                pf.write(f"# Prompt template for {section['number']}. {section['title']}\n\n")
                pf.write(subsection_summary)
                pf.write(chapter_prompt_template.replace("{chapter}", f"{section['number']}. {section['title']}"))
            prompt_paths.append(prompt_path)
            if "subsections" in section and section["subsections"]:
                prompt_paths.extend(traverse_sections(section["subsections"], generated_prompts_dir, chapter_prompt_template))
        return prompt_paths
    generated_prompts_dir = os.path.join(state.repo_root, "prompts", "generated")
    chapter_prompt_template = state.chapter_prompt_text.strip()
    traverse_sections(state.toc_dict["chapters"], generated_prompts_dir, chapter_prompt_template)
    return state

# --- Node: Pause for prompt review ---
def review_prompts_node(state):
    input("Review and edit the generated section prompt templates in 'prompts/generated/'. Press Enter to continue...")
    return state

# --- Node: Generate content for all sections ---
def generate_content_node(state):
    def traverse_content(sections, generated_prompts_dir, gemini_llm, directory, chapter_prompt_template):
        for section in sections:
            safe_section_number = section["number"].replace('.', '_')
            prompt_filename = f"section_{safe_section_number}_prompt.txt"
            prompt_path = os.path.join(generated_prompts_dir, prompt_filename)
            with open(prompt_path, "r", encoding="utf-8") as pf:
                section_prompt = pf.read()
            section_template = PromptTemplate(
                input_variables=["chapter"],
                template=section_prompt,
            )
            section_chain = section_template | gemini_llm
            section_heading = f"{section['number']}. {section['title']}"
            print(f"\nGenerating content for section: {section_heading}")
            section_raw = section_chain.invoke({"chapter": section_heading})
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
            if "subsections" in section and section["subsections"]:
                traverse_content(section["subsections"], generated_prompts_dir, gemini_llm, directory, chapter_prompt_template)
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
    )
    generated_prompts_dir = os.path.join(state.repo_root, "prompts", "generated")
    traverse_content(state.toc_dict["chapters"], generated_prompts_dir, gemini_llm, state.output_dir, state.chapter_prompt_text)
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
def run_book_graph(topic, chapter_count, output_dir, sub_topics, chapter_prompt_text, toc_prompt_text):
    repo_root = os.path.dirname(os.path.dirname(__file__))
    state = {
        "topic": topic,
        "chapter_count": chapter_count,
        "output_dir": output_dir,
        "sub_topics": sub_topics,
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
    parser.add_argument("--subtopics", default="", help="Comma-separated subtopics")
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
        sub_topics=args.subtopics,
        chapter_prompt_text=chapter_prompt_text,
        toc_prompt_text=toc_prompt_text,
    )
