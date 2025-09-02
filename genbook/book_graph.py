
# Refactored: Use new modular pipeline
from genbook.graph_state import StateModel
from genbook.toc_generation import generate_toc_node, write_toc_node, review_toc_node
from genbook.prompt_generation import write_prompts_node, review_prompts_node
from genbook.content_generation import generate_content_node
from langgraph.graph import StateGraph

def build_book_graph():
    graph = StateGraph(StateModel)
    graph.add_node("generate_toc", generate_toc_node)
    graph.add_node("write_toc", write_toc_node)
    graph.add_node("review_toc", review_toc_node)
    graph.add_node("write_prompts", write_prompts_node)
    graph.add_node("review_prompts", review_prompts_node)
    graph.add_node("generate_content", generate_content_node)
    graph.add_node("end", lambda state: print("Book generation complete.") or state)
    graph.add_edge("generate_toc", "write_toc")
    graph.add_edge("write_toc", "review_toc")
    graph.add_edge("review_toc", "write_prompts")
    graph.add_edge("write_prompts", "review_prompts")
    graph.add_edge("review_prompts", "generate_content")
    graph.add_edge("generate_content", "end")
    graph.set_entry_point("generate_toc")
    return graph

def run_book_graph(topic, chapter_count, output_dir, chapter_prompt_text, toc_prompt_text, chapter_length="medium", section_length="medium", toc_length="medium"):
    import os
    repo_root = os.path.dirname(os.path.dirname(__file__))
    state = {
        "topic": topic,
    "chapter_count": int(chapter_count),
        "output_dir": output_dir,
        "chapter_prompt_text": chapter_prompt_text,
        "toc_prompt_text": toc_prompt_text,
        "repo_root": repo_root,
        "chapter_length": chapter_length,
        "section_length": section_length,
        "toc_length": toc_length,
    }
    graph = build_book_graph()
    compiled_graph = graph.compile()
    compiled_graph.invoke(state)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Gemini Book Generator with LangGraph")
    parser.add_argument("--topic", required=True, help="Book topic")
    parser.add_argument("--chapter-count", required=True, help="Number of chapters")
    parser.add_argument("--output-dir", required=True, help="Output directory for markdown files")
    parser.add_argument("--chapter-length", default="medium", help="Desired chapter length (short, medium, long, or word count)")
    parser.add_argument("--section-length", default="medium", help="Desired section length (short, medium, long, or word count)")
    parser.add_argument("--toc-length", default="medium", help="Desired ToC detail level (short, medium, long, or number of sections/levels)")
    parser.add_argument("--chapter-prompt-file", required=True, help="Path to chapter prompt template file")
    parser.add_argument("--toc-prompt-file", required=True, help="Path to ToC prompt template file")
    args = parser.parse_args()
    with open(args.chapter_prompt_file, "r", encoding="utf-8") as f:
        chapter_prompt_text = f.read()
    with open(args.toc_prompt_file, "r", encoding="utf-8") as f:
        toc_prompt_text = f.read()
    run_book_graph(
        topic=args.topic,
        chapter_count=args.chapter_count,
        output_dir=args.output_dir,
        chapter_prompt_text=chapter_prompt_text,
        toc_prompt_text=toc_prompt_text,
        chapter_length=args.chapter_length,
        section_length=args.section_length,
        toc_length=args.toc_length,
    )
