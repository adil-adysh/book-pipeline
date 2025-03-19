from _typeshed import Incomplete
from ebooklib.plugins.base import BasePlugin as BasePlugin
from ebooklib.utils import parse_html_string as parse_html_string

class BooktypeLinks(BasePlugin):
    NAME: str
    booktype_book: Incomplete
    def __init__(self, booktype_book) -> None: ...
    def html_before_write(self, book, chapter) -> None: ...

class BooktypeFootnotes(BasePlugin):
    NAME: str
    booktype_book: Incomplete
    def __init__(self, booktype_book) -> None: ...
    def html_before_write(self, book, chapter) -> None: ...
