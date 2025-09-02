from pydantic import BaseModel
from typing import Optional, Dict, Any

class StateModel(BaseModel):
    topic: str
    chapter_count: str
    output_dir: str
    chapter_prompt_text: str
    toc_prompt_text: str
    repo_root: str
    chapter_length: str = "medium"
    section_length: str = "medium"
    toc_length: str = "medium"
    toc_dict: Optional[Dict[str, Any]] = None
    toc_json_path: Optional[str] = None
