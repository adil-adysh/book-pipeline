import os
from typing import List

def write_prompts_node(state):
    from gemini_book_generator.graph_state import StateModel
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    section_prompt_path = os.path.join(state.repo_root, "gemini_book_generator", "prompts", "section_prompt.txt")
    def traverse_sections(sections, book_title, chapter_title, chapter_summary, section_prompt_template, section_length, previous_titles=None, seen_sections=None):
        if previous_titles is None:
            previous_titles = []
        if seen_sections is None:
            seen_sections = set()
        prompt_paths = []
        for idx, section in enumerate(sections):
            section_id = (section["number"], section["title"])
            if section_id in seen_sections:
                continue
            seen_sections.add(section_id)
            safe_section_number = section["number"].replace('.', '_')
            prompt_filename = f"section_{safe_section_number}_prompt.txt"
            prompt_path = os.path.join(generated_prompts_dir, prompt_filename)
            subsection_summary = ""
            if "subsections" in section and section["subsections"]:
                subsection_summary = "\nSubsections:\n" + "\n".join([
                    f"- {sub['number']}: {sub['title']}" for sub in section["subsections"]
                ]) + "\n"
            prev_sections = previous_titles.copy()
            prompt_vars = {
                "book_title": book_title,
                "chapter_title": chapter_title,
                "chapter_summary": chapter_summary,
                "section_title": section["title"],
                "section_number": section["number"],
                "section_length": section_length,
                "previous_sections": "; ".join(prev_sections) if prev_sections else "None",
            }
            with open(section_prompt_path, "r", encoding="utf-8") as f:
                section_prompt_template = f.read()
            prompt_text = section_prompt_template
            for k, v in prompt_vars.items():
                prompt_text = prompt_text.replace(f"{{{{{k}}}}}", str(v)).replace(f"{{{k}}}", str(v))
            prompt_text = prompt_text + "\n\nInstructions for AI: Keep the section concise and focused. Aim for brevity and clarity."
            with open(prompt_path, "w", encoding="utf-8") as pf:
                pf.write(f"# Prompt template for {section['number']}. {section['title']}\n\n")
                pf.write(subsection_summary)
                pf.write(prompt_text)
            prompt_paths.append(prompt_path)
            if "subsections" in section and section["subsections"]:
                prompt_paths.extend(traverse_sections(section["subsections"], book_title, chapter_title, chapter_summary, section_prompt_template, section_length, prev_sections + [section["title"]], seen_sections))
        return prompt_paths
    chapter_prompt_path_template = os.path.join(generated_prompts_dir, "chapter_{chapter_number}_prompt.txt")
    chapter_prompt_template_path = os.path.join(state.repo_root, "gemini_book_generator", "prompts", "chapter_prompt.txt")
    with open(chapter_prompt_template_path, "r", encoding="utf-8") as f:
        chapter_prompt_template = f.read()
    book_title = state.topic
    chapters = state.toc_dict["chapters"]
    for chapter in chapters:
        chapter_title = chapter["title"]
        chapter_summary = chapter.get("summary", "")
        chapter_number = chapter["number"] if "number" in chapter else ""
        chapter_vars = {
            "book_title": book_title,
            "book_summary": "",
            "chapter_title": chapter_title,
            "chapter_number": chapter_number,
            "previous_chapter_summary": "",
            "chapter_length": state.chapter_length,
        }
        prompt_text = chapter_prompt_template
        for k, v in chapter_vars.items():
            prompt_text = prompt_text.replace(f"{{{{{k}}}}}", str(v)).replace(f"{{{k}}}", str(v))
        chapter_prompt_path = chapter_prompt_path_template.format(chapter_number=chapter_number.replace('.', '_'))
        with open(chapter_prompt_path, "w", encoding="utf-8") as pf:
            pf.write(f"# Prompt template for chapter {chapter_number}: {chapter_title}\n\n")
            pf.write(prompt_text)
        traverse_sections(chapter.get("subsections", [chapter]), book_title, chapter_title, chapter_summary, None, "short", [], set())
    return state

def review_prompts_node(state):
    input("Review and edit the generated section and chapter prompt templates in 'generated-prompts/'. Press Enter to continue...")
    return state
