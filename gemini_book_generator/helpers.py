import os


# --- Helper to Get File Path Relative to This Script ---
def get_prompt_file_path(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(current_dir, "prompts")
    return os.path.join(prompts_dir, file_name)


# --- Helper to Load Prompts from Files ---
def load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


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
        if (f.startswith("chapter_") or f.startswith("section_")) and f.endswith(".md")
    ]
    files.sort(key=extract_chapter_key)
    return files
