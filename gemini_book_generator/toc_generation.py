import os
import json
from langchain_core.prompts import PromptTemplate
from gemini_llm import GeminiLLM

def generate_toc_node(state):
    gemini_llm = GeminiLLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-2.0-flash",
        temperature=0.7,
    )
    toc_template = PromptTemplate(
        input_variables=["topic", "chapterCount", "toc_length"],
        template=state.toc_prompt_text,
    )
    toc_chain = toc_template | gemini_llm
    toc_raw = toc_chain.invoke({
        "topic": state.topic,
        "chapterCount": state.chapter_count,
        "toc_length": state.toc_length,
    })
    toc_text = toc_raw
    if toc_text.startswith("```json"):
        toc_text = toc_text.replace("```json", "", 1)
    if toc_text.endswith("```"):
        toc_text = toc_text.rsplit("```", 1)[0]
    toc_text = toc_text.strip()
    toc_dict = json.loads(toc_text)
    state.toc_dict = toc_dict
    return state

def write_toc_node(state):
    generated_prompts_dir = os.path.join(state.repo_root, "generated-prompts")
    os.makedirs(generated_prompts_dir, exist_ok=True)
    toc_json_path = os.path.join(generated_prompts_dir, "book_index.json")
    with open(toc_json_path, "w", encoding="utf-8") as f:
        json.dump(state.toc_dict, f, indent=2)
    state.toc_json_path = toc_json_path
    return state

def review_toc_node(state):
    input(f"Review and edit the generated Table of Contents in '{state.toc_json_path}' (located in 'generated-prompts'). Press Enter to continue...")
    with open(state.toc_json_path, "r", encoding="utf-8") as f:
        state.toc_dict = json.load(f)
    return state
