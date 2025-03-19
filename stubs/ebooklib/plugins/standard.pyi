from _typeshed import Incomplete
from ebooklib.plugins.base import BasePlugin as BasePlugin
from ebooklib.utils import parse_html_string as parse_html_string

ATTRIBUTES_GLOBAL: Incomplete
DEPRECATED_TAGS: Incomplete

def leave_only(item, tag_list) -> None: ...

class SyntaxPlugin(BasePlugin):
    NAME: str
    def html_before_write(self, book, chapter): ...
