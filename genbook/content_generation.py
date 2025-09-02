import os
from genbook.gemini_llm import GeminiLLM

def generate_content_node(state):
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    section_prompt_path = os.path.join(state.repo_root, "genbook", "prompts", "section_prompt.txt")
    # Lazy import for PromptTemplate to allow running without langchain_core installed
    try:
        from langchain_core.prompts import PromptTemplate
    except Exception:
        PromptTemplate = None
    def get_chapter_prompt_path(chapter_number: str) -> str:
        safe_chapter_number = chapter_number.replace('.', '_')
        return os.path.join(generated_prompts_dir, f"chapter_{safe_chapter_number}_prompt.txt")
    def pad_section_number(section_number: str, width: int = 3) -> str:
        parts = section_number.split('.')
        return '_'.join([str(part).zfill(width) for part in parts])
    def traverse_content(sections, gemini_llm, directory, section_prompt_template, book_title, chapter_title, chapter_summary, section_length):
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
                "section_length": section_length,
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
            # Also write to project-level chapters directory so the project contains generated markdown
            project_root = getattr(state, "project_root", os.path.dirname(directory))
            project_chapters_dir = os.path.join(project_root, "chapters")
            os.makedirs(project_chapters_dir, exist_ok=True)
            project_section_md_path = os.path.join(project_chapters_dir, markdown_filename)
            base_path = section_md_path
            suffix = 1
            while os.path.exists(section_md_path):
                section_md_path = base_path.replace('.md', f'_{suffix}.md')
                suffix += 1
            with open(section_md_path, "w", encoding="utf-8") as f:
                f.write(f"# {section_heading}\n\n")
                f.write(section_content)
            # mirror to project chapters dir
            with open(project_section_md_path, "w", encoding="utf-8") as f2:
                f2.write(f"# {section_heading}\n\n")
                f2.write(section_content)
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
                    section_length,
                )
    def generate_chapter(chapter, gemini_llm, output_dir, chapter_prompt_template, book_title, book_summary, previous_chapter_summary, chapter_length):
        chapter_vars = {
            "book_title": book_title,
            "book_summary": book_summary,
            "chapter_title": chapter["title"],
            "chapter_number": chapter["number"] if "number" in chapter else "",
            "previous_chapter_summary": previous_chapter_summary,
            "chapter_length": chapter_length,
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
        # Also ensure project-level chapters directory
        project_root = getattr(state, "project_root", os.path.dirname(output_dir))
        project_chapters_dir = os.path.join(project_root, "chapters")
        os.makedirs(project_chapters_dir, exist_ok=True)
        project_chapter_md_path = os.path.join(project_chapters_dir, markdown_filename)
        with open(chapter_md_path, "w", encoding="utf-8") as f:
            f.write(f"# {chapter_vars['chapter_title']}\n\n")
            f.write(chapter_content)
        # mirror to project chapters dir
        with open(project_chapter_md_path, "w", encoding="utf-8") as f2:
            f2.write(f"# {chapter_vars['chapter_title']}\n\n")
            f2.write(chapter_content)
        print(f"Saved {chapter_md_path} and {project_chapter_md_path}")
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
    )
    with open(section_prompt_path, "r", encoding="utf-8") as f:
        section_prompt_template = f.read()
    book_title = state.topic
    book_summary = ""
    chapters = state.toc_dict["chapters"]
    previous_chapter_summary = ""
    for chapter in chapters:
        chapter_number = chapter["number"] if "number" in chapter else ""
        chapter_prompt_path = get_chapter_prompt_path(chapter_number)
        with open(chapter_prompt_path, "r", encoding="utf-8") as f:
            chapter_prompt_template = f.read()

        generate_chapter(
            chapter,
            gemini_llm,
            state.output_dir,
            chapter_prompt_template,
            book_title,
            book_summary,
            previous_chapter_summary,
            state.chapter_length,
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
            state.section_length,
        )
    return state
