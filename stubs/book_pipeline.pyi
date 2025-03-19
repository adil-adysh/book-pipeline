from _typeshed import Incomplete
from pydantic import BaseModel

class ChapterModel(BaseModel):
    number: str
    title: str

class ToC(BaseModel):
    chapters: list[ChapterModel]

toc_parser: Incomplete

def generate_book_pipeline(topic: str, chapter_count: str, directory: str, sub_topics: str, chapter_prompt_text: str, toc_prompt_text: str): ...
