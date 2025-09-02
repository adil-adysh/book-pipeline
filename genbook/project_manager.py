import os
import json
from typing import Dict, Any

class BookProject:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.config_path = os.path.join(project_root, "book_config.json")
        self.prompts_dir = os.path.join(project_root, "prompts")
        self.generated_dir = os.path.join(project_root, "generated")
        self.epub_dir = os.path.join(project_root, "epub")
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
        os.makedirs(self.epub_dir, exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def init_project(self, topic: str, chapter_count: int):
        self.config["topic"] = topic
        self.config["chapter_count"] = chapter_count
        self.config["status"] = "initialized"
        self.save_config()

    def cache_exists(self, key: str) -> bool:
        return self.config.get("cache", {}).get(key, False)

    def set_cache(self, key: str, value: bool):
        if "cache" not in self.config:
            self.config["cache"] = {}
        self.config["cache"][key] = value
        self.save_config()

    def get_status(self) -> str:
        return self.config.get("status", "unknown")

    def update_status(self, status: str):
        self.config["status"] = status
        self.save_config()

    def get_metadata(self) -> Dict[str, Any]:
        return self.config

    # Add more project management methods as needed
