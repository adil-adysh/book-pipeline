import os
import json
from typing import Optional

import typer

from genbook.project_manager import BookProject

app = typer.Typer(name="genbook", help="GenBook CLI")


def _confirm_overwrite(path: str) -> bool:
    if not os.path.exists(path):
        return True
    return typer.confirm(f"Directory '{path}' already exists. Overwrite config?")


def _resolve_project_dir(project_dir: Optional[str]) -> str:
    """Return project_dir if given, otherwise use cwd when it looks like a project."""
    if project_dir:
        return project_dir
    cwd = os.getcwd()
    looks_like_project = os.path.exists(os.path.join(cwd, "book_config.json")) or os.path.exists(
        os.path.join(cwd, "prompts")
    )
    if looks_like_project:
        return cwd
    raise typer.BadParameter("--project-dir is required unless you run the command inside a project folder")


@app.command()
def create(
    project_dir: Optional[str] = typer.Option(None, help="Path to project directory"),
    topic: Optional[str] = typer.Option(None, help="Book topic"),
    chapter_count: Optional[int] = typer.Option(None, help="Number of chapters"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Automatic yes to prompts"),
):
    """Create a new book project interactively."""
    # If user runs the command inside an existing project directory, use cwd
    if not project_dir:
        cwd = os.getcwd()
        looks_like_project = os.path.exists(os.path.join(cwd, "book_config.json")) or os.path.exists(
            os.path.join(cwd, "prompts")
        )
        if looks_like_project:
            project_dir = cwd
        else:
            project_dir = typer.prompt("Project directory (path)", default="./new_book")
    if not topic:
        topic = typer.prompt("Book topic")
    if chapter_count is None:
        chapter_count = typer.prompt("Number of chapters", type=int)

    if not yes and not _confirm_overwrite(project_dir):
        typer.echo("Aborted by user.")
        raise typer.Exit(code=1)

    os.makedirs(project_dir, exist_ok=True)
    project = BookProject(project_dir)
    project.init_project(topic, chapter_count)
    typer.echo(f"Project created at: {project.project_root}")
    typer.echo("Next steps:")
    typer.echo(f"  - Edit prompts in {project.prompts_dir} if desired")
    typer.echo(
        f"  - Run generation: genbook generate --project-dir {project.project_root} --chapter-prompt-file <path> --toc-prompt-file <path>"
    )


@app.command()
def status(project_dir: Optional[str] = typer.Option(None, help="Path to project directory")):
    """Show project configuration and metadata."""
    proj_dir = _resolve_project_dir(project_dir)
    project = BookProject(proj_dir)
    typer.echo(json.dumps(project.get_metadata(), indent=2))


@app.command()
def edit(
    project_dir: Optional[str] = typer.Option(None, help="Path to project directory"),
    topic: Optional[str] = typer.Option(None, help="New topic"),
    chapter_count: Optional[int] = typer.Option(None, help="New chapter count"),
):
    """Edit project metadata (topic, chapter_count)."""
    proj_dir = _resolve_project_dir(project_dir)
    project = BookProject(proj_dir)
    if topic:
        project.config["topic"] = topic
    if chapter_count is not None:
        project.config["chapter_count"] = int(chapter_count)
    project.save_config()
    typer.echo(f"Project updated at: {project.project_root}")


@app.command()
def generate(
    project_dir: Optional[str] = typer.Option(None, help="Path to project directory"),
    chapter_prompt_file: Optional[str] = typer.Option(None, help="Path to chapter prompt template"),
    toc_prompt_file: Optional[str] = typer.Option(None, help="Path to ToC prompt template"),
    chapter_length: str = typer.Option("medium"),
    section_length: str = typer.Option("medium"),
    toc_length: str = typer.Option("medium"),
):
    """Run the generation graph for the specified project."""
    proj_dir = _resolve_project_dir(project_dir)
    project = BookProject(proj_dir)

    # Resolve prompt files: use provided path, otherwise use project's prompts
    if chapter_prompt_file:
        chapter_prompt_path = chapter_prompt_file
    else:
        chapter_prompt_path = os.path.join(project.prompts_dir, "chapter_prompt.txt")
    if toc_prompt_file:
        toc_prompt_path = toc_prompt_file
    else:
        toc_prompt_path = os.path.join(project.prompts_dir, "toc_prompt.txt")

    with open(chapter_prompt_path, "r", encoding="utf-8") as f:
        chapter_prompt_text = f.read()
    with open(toc_prompt_path, "r", encoding="utf-8") as f:
        toc_prompt_text = f.read()

    # Lazy import of the graph runner to avoid hard dependency at CLI import time
    try:
        from genbook.book_graph import run_book_graph as book_run_book_graph
    except Exception:
        typer.echo("Could not import generation graph. Ensure 'langgraph' is installed to run generation.")
        raise typer.Exit(code=2)

    topic = project.config.get("topic")
    chapter_count = project.config.get("chapter_count")
    output_dir = project.generated_dir
    book_run_book_graph(
        topic,
        chapter_count,
        output_dir,
        chapter_prompt_text,
        toc_prompt_text,
        chapter_length=chapter_length,
        section_length=section_length,
        toc_length=toc_length,
    )


def main():
    app()


if __name__ == "__main__":
    main()
