"""Smoke runner: runs the book graph with stubbed LLM and PromptTemplate to generate predictable outputs.
This avoids external API calls and verifies that generated prompts and markdown files are written into the project.
"""
import os
import sys
from types import SimpleNamespace

# Add repo root to PYTHONPATH
repo_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, repo_root)

from genbook.book_graph import run_book_graph

# Create deterministic chapter and toc prompt texts
chapter_prompt_text = "CHAPTER_PROMPT_TEMPLATE"
toc_prompt_text = "TOC_PROMPT_TEMPLATE"

# Choose an example project inside the repo
project_dir = os.path.join(repo_root, "apple")
generated_prompts_dir = os.path.join(project_dir, "generated-prompts")

# Ensure output dir exists
os.makedirs(generated_prompts_dir, exist_ok=True)

# Use small sample topic and chapter count
topic = "smoke-test"
chapter_count = 1

# Run the graph. The project uses the local GeminiLLM class which will attempt to call external API.
# To avoid that, we monkeypatch genbook.gemini_llm.GeminiLLM to a stub that implements minimal interface.
import genbook

# Insert a stub GeminiLLM before importing book_graph internals
from genbook import gemini_llm as _gemini_mod

class StubLLM:
    def __init__(self, *args, **kwargs):
        pass
    def __ror__(self, other):
        # allow PromptTemplate | StubLLM chaining by returning self
        return self
    def invoke(self, prompt_vars):
        # Return a fixed string using available vars
        if isinstance(prompt_vars, dict):
            if 'section_title' in prompt_vars:
                return f"Generated content for {prompt_vars.get('section_title')}"
            if 'chapter_title' in prompt_vars:
                return f"Generated chapter content for {prompt_vars.get('chapter_title')}"
        return 'OK'

_gemini_mod.GeminiLLM = StubLLM

# Also stub PromptTemplate used in modules to avoid importing langchain
class StubPromptTemplate:
    def __init__(self, input_variables=None, template=None):
        self.input_variables = input_variables or []
        self.template = template or ""
    def __or__(self, other):
        return other
    def invoke(self, vars):
        # Simulate rendering by simple replacement
        if isinstance(vars, dict):
            return f"Rendered: {vars.get('chapter_title') or vars.get('section_title') or vars.get('topic')}"
        return "Rendered"

# Monkeypatch langchain_core.prompts.PromptTemplate if the module exists; otherwise, insert into sys.modules
try:
    import langchain_core.prompts as _lc_prompts
    _lc_prompts.PromptTemplate = StubPromptTemplate
except Exception:
    import types
    mod = types.SimpleNamespace(PromptTemplate=StubPromptTemplate)
    sys.modules['langchain_core.prompts'] = mod

# Finally run the book graph
print('Running smoke graph...')
run_book_graph(topic, chapter_count, generated_prompts_dir, chapter_prompt_text, toc_prompt_text)
print('Smoke run complete. Files created in:', generated_prompts_dir)

# List generated files
for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith('.md') or f.endswith('_prompt.txt') or f.endswith('.json'):
            print(os.path.join(root, f))
