import os
import tempfile
import json
from gemini_book_generator import epub_generator

def test_epub_generation_minimal():
    # Setup temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal book_index.json
        toc = {
            "chapters": [
                {"number": "1", "title": "Test Chapter", "subsections": []}
            ]
        }
        toc_path = os.path.join(tmpdir, "book_index.json")
        with open(toc_path, "w", encoding="utf-8") as f:
            json.dump(toc, f)
        # Create minimal chapter markdown file
        chapter_md_path = os.path.join(tmpdir, "section_001.md")
        with open(chapter_md_path, "w", encoding="utf-8") as f:
            f.write("# Test Chapter\n\nThis is a test chapter.")
        # Run EPUB generation
        epub_path = os.path.join(tmpdir, "test_book.epub")
        epub_generator.create_epub_from_md(
            epub_filename=epub_path,
            book_title="Minimal Test Book",
            directory=tmpdir
        )
        # Check that EPUB file was created
        assert os.path.exists(epub_path)
        print(f"EPUB generated at: {epub_path}")
