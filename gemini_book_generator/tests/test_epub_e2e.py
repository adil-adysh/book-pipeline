import os
import tempfile
import json
from gemini_book_generator import epub_generator

def create_md_files_from_toc(toc, directory):
    """Recursively create .md files for all chapters and sections in the ToC."""
    def pad_section_number(section_number, width=3):
        parts = section_number.split('.')
        return '_'.join([str(p).zfill(width) for p in parts])
    def create_section(section):
        filename = f"section_{pad_section_number(section['number'])}.md"
        path = os.path.join(directory, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {section['title']}\n\nContent for {section['title']}.")
        for sub in section.get('subsections', []):
            create_section(sub)
    for chapter in toc['chapters']:
        create_section(chapter)

def test_epub_e2e():
    # Setup temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Minimal ToC with nested sections
        toc = {
            "chapters": [
                {
                    "number": "1",
                    "title": "Test Chapter",
                    "subsections": [
                        {
                            "number": "1.1",
                            "title": "Section 1.1",
                            "subsections": [
                                {
                                    "number": "1.1.1",
                                    "title": "Section 1.1.1"
                                }
                            ]
                        },
                        {
                            "number": "1.2",
                            "title": "Section 1.2"
                        }
                    ]
                }
            ]
        }
        toc_path = os.path.join(tmpdir, "book_index.json")
        with open(toc_path, "w", encoding="utf-8") as f:
            json.dump(toc, f)
        # Create all required .md files
        create_md_files_from_toc(toc, tmpdir)
        # Run EPUB generation
        epub_path = os.path.join(tmpdir, "test_book_e2e.epub")
        epub_generator.create_epub_from_md(
            epub_filename=epub_path,
            book_title="E2E Test Book",
            directory=tmpdir
        )
        # Check that EPUB file was created
        assert os.path.exists(epub_path)
        print(f"E2E EPUB generated at: {epub_path}")
