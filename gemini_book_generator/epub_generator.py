import os
import markdown
import json
from ebooklib import epub
from .helpers import get_sorted_chapter_files


def create_style_sheet(book):
    """Create and add a CSS style sheet to the EPUB book."""
    style_content = "body { font-family: Times, Times New Roman, serif; }"
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style_content,
    )
    book.add_item(nav_css)
    return nav_css


def process_introduction(book, directory, nav_css):
    """Process the introduction chapter from 'book_index.md' if available."""
    index_path = os.path.join(directory, "book_index.md")
    if not os.path.exists(index_path):
        print("No book_index.md found for introduction.")
        return None
    with open(index_path, "r", encoding="utf-8") as f:
        index_md = f.read()
    index_html = markdown.markdown(index_md)
    intro_item = epub.EpubHtml(title="Introduction", file_name="intro.xhtml", lang="en")
    intro_item.set_content(f"<html><body>{index_html}</body></html>")
    intro_item.add_item(nav_css)
    book.add_item(intro_item)
    print(f"Added introduction from {index_path}.")
    return intro_item


def process_chapters(book, directory, nav_css):
    """Process chapter Markdown files from the directory and return chapter items."""
    chapter_files = get_sorted_chapter_files(directory)
    print("Chapter files found:", chapter_files)
    chapter_items = []
    for md_file in chapter_files:
        md_path = os.path.join(directory, md_file)
        with open(md_path, "r", encoding="utf-8") as f:
            chapter_md = f.read()
        chapter_html = markdown.markdown(chapter_md)
        chapter_title = os.path.splitext(md_file)[0]
        chapter_item = epub.EpubHtml(
            title=chapter_title, file_name=md_file.replace(".md", ".xhtml"), lang="en"
        )
        chapter_item.set_content(
            f"<html><body><h1>{chapter_title}</h1>{chapter_html}</body></html>"
        )
        chapter_item.add_item(nav_css)
        book.add_item(chapter_item)
        chapter_items.append(chapter_item)
        print(f"Added chapter: {chapter_title} from {md_path}.")
    return chapter_items


def build_toc(book, intro_item, chapter_items):
    """Build the table of contents (ToC) for the book."""
    # Try to load hierarchical ToC from book_index.json
    # Use the directory where markdown and JSON files are located
    import inspect
    frame = inspect.currentframe()
    directory = None
    while frame:
        if 'directory' in frame.f_locals:
            directory = frame.f_locals['directory']
            break
        frame = frame.f_back
    if directory is None:
        directory = '.'
    toc_json_path = os.path.join(directory, "book_index.json")
    if not os.path.exists(toc_json_path):
        # Fallback to flat ToC
        toc_entries = []
        if intro_item is not None:
            toc_entries.append(epub.Link(intro_item.file_name, "Introduction", "intro"))
        if chapter_items:
            toc_entries.append((epub.Section("Chapters"), tuple(chapter_items)))
        book.toc = tuple(toc_entries)
        return

    with open(toc_json_path, "r", encoding="utf-8") as f:
        toc_dict = json.load(f)

    def find_md_item(section_number):
        # Zero-pad section number for filename matching
        parts = section_number.split('.')
        padded = '_'.join([str(p).zfill(3) for p in parts])
        filename = f"section_{padded}.md"
        xhtml = filename.replace('.md', '.xhtml')
        for item in chapter_items:
            if item.file_name == xhtml:
                return item
        return None

    def build_section(section):
        item = find_md_item(section["number"])
        children = []
        if "subsections" in section and section["subsections"]:
            for sub in section["subsections"]:
                child = build_section(sub)
                if child:
                    children.append(child)
        if item:
            if children:
                return (epub.Section(f"{section['number']}. {section['title']}"), tuple(children + [item]))
            else:
                return item
        return None

    toc_entries = []
    if intro_item is not None:
        toc_entries.append(epub.Link(intro_item.file_name, "Introduction", "intro"))
    if "chapters" in toc_dict:
        for chapter in toc_dict["chapters"]:
            entry = build_section(chapter)
            if entry:
                toc_entries.append(entry)
    book.toc = tuple(toc_entries)


def build_spine(book, intro_item, chapter_items):
    """Build the spine (reading order) for the book."""
    spine = ["nav"]
    if intro_item is not None:
        spine.append(intro_item)
    spine.extend(chapter_items)
    book.spine = spine


def create_epub_from_md(
    epub_filename: str,
    book_title: str,
    book_author: str = "gemini",
    book_description: str = "",
    directory=".",
):
    """Create an EPUB from Markdown files in the specified directory."""
    # Initialize the book and set minimal metadata.
    book = epub.EpubBook()
    book.set_identifier("sample123456")
    book.set_title(book_title)
    book.set_language("en")
    book.add_author(book_author)
    book.add_metadata("DC", "description", book_description)
    book.add_metadata(None, "meta", "", {"name": "key", "content": "value"})

    # Create and add the CSS style sheet.
    nav_css = create_style_sheet(book)

    # Process introduction and chapter files.
    intro_item = process_introduction(book, directory, nav_css)
    chapter_items = process_chapters(book, directory, nav_css)

    # Build the Table of Contents and the spine.
    build_toc(book, intro_item, chapter_items)
    build_spine(book, intro_item, chapter_items)

    # Add navigation files (NCX and EPUB3 Navigation).
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Write the EPUB file.
    epub.write_epub(epub_filename, book, {})
    print(f"EPUB created successfully: {epub_filename}")
