import os
import json
import shutil
from typing import Dict, Any


class BookProject:
    """Utility class to manage a book project on disk.

    Responsibilities:
    - Create project directory layout (prompts/, generated/, epub/, src files)
    - Initialize a minimal `book_config.json` with topic and chapter_count
    - Copy bundled prompt templates from package `genbook/prompts/` into project prompts
    """

    def __init__(self, project_root: str):
        self.project_root = os.path.abspath(project_root)
        self.config_path = os.path.join(self.project_root, "book_config.json")
        self.prompts_dir = os.path.join(self.project_root, "prompts")
        self.generated_dir = os.path.join(self.project_root, "generated-prompts")
        self.epub_dir = os.path.join(self.project_root, "epub")

        # Ensure directories exist
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)
        os.makedirs(self.epub_dir, exist_ok=True)

        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except Exception:
                    return {}
        return {}

    def save_config(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def init_project(self, topic: str, chapter_count: int) -> None:
        """Create initial project files and configuration.

        This will:
        - write topic and chapter_count to `book_config.json`
        - copy packaged prompt templates from `genbook/prompts/` into the project's `prompts/`
        """
        self.config["topic"] = topic
        self.config["chapter_count"] = int(chapter_count)
        self.config["status"] = "initialized"
        self.save_config()

        # Copy default prompts bundled with the package into the project prompts dir
        bundled_prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
        if os.path.isdir(bundled_prompts_dir):
            for name in os.listdir(bundled_prompts_dir):
                src = os.path.join(bundled_prompts_dir, name)
                dst = os.path.join(self.prompts_dir, name)
                # only copy files, don't overwrite existing files
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copyfile(src, dst)

    def cache_exists(self, key: str) -> bool:
        return bool(self.config.get("cache", {}).get(key, False))

    def set_cache(self, key: str, value: bool) -> None:
        if "cache" not in self.config:
            self.config["cache"] = {}
        self.config["cache"][key] = bool(value)
        self.save_config()

    def get_status(self) -> str:
        return self.config.get("status", "unknown")

    def update_status(self, status: str) -> None:
        self.config["status"] = status
        self.save_config()

    def get_metadata(self) -> Dict[str, Any]:
        return self.config

    # Convenience properties used by other modules
    @property
    def project_root_dir(self) -> str:
        return self.project_root

    @property
    def generated_dir_path(self) -> str:
        return self.generated_dir

    @property
    def prompts_dir_path(self) -> str:
        return self.prompts_dir

