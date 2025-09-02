import tempfile
import os
import json
from genbook.project_manager import BookProject


def test_init_project_creates_structure(tmp_path):
    project_dir = tmp_path / "mybook"
    project_dir.mkdir()
    bp = BookProject(str(project_dir))
    # init project
    bp.init_project(topic="Test Topic", chapter_count=3)

    # verify config
    config_path = project_dir / "book_config.json"
    assert config_path.exists(), "book_config.json should be created"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    assert cfg.get("topic") == "Test Topic"
    assert int(cfg.get("chapter_count")) == 3

    # verify prompts dir exists
    prompts_dir = project_dir / "prompts"
    assert prompts_dir.exists() and prompts_dir.is_dir()

    # if package has bundled prompts, at least the directory is present
    # generated-prompts and epub should also exist
    assert (project_dir / "generated-prompts").exists()
    assert (project_dir / "epub").exists()

    # cleanup is automatic via tmp_path
