import os
import markdown
from ebooklib import epub
from helpers import get_sorted_chapter_files


def create_epub_from_md(epub_filename: str, book_title: str, directory="."):
    book = epub.EpubBook()
    book.set_title(book_title)
    book.set_language("en")

    spine = ["nav"]

    # Add the book index if it exists (assumed as preface/intro)
    index_path = os.path.join(directory, "book_index.md")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
        index_html = markdown.markdown(index_content)
        index_item = epub.EpubHtml(
            title="Table of Contents", file_name="index.xhtml", content=index_html
        )
        book.add_item(index_item)
        spine.append(index_item.file_name)

    # Process chapter Markdown files
    chapter_files = get_sorted_chapter_files(directory)
    for md_file in chapter_files:
        with open(os.path.join(directory, md_file), "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        chapter_title = os.path.splitext(md_file)[0]
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=md_file.replace(".md", ".xhtml"),
            content=html_content,
        )
        book.add_item(chapter)
        spine.append(chapter.file_name)

    book.toc = tuple(spine[1:])  # Skip the 'nav' element
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Optionally add CSS styling
    style = "body { font-family: Arial, sans-serif; }"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    book.spine = spine
    epub.write_epub(epub_filename, book, {})
    print(f"EPUB created: {epub_filename}")
