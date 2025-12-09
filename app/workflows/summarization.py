from typing import Dict, Any, List
from ..engine.registry import registry


def split_text_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    text = state.get("text", "")
    max_chunk_size = state.get("max_chunk_size", 200)

    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    state["chunks"] = chunks
    return state


def summarize_chunks_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    chunks: List[str] = state.get("chunks", [])
    summaries: List[str] = []

    # naive summaries: just first 100 chars of each chunk
    for chunk in chunks:
        summaries.append(chunk[:100])

    state["summaries"] = summaries
    return state


def merge_summaries_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    summaries: List[str] = state.get("summaries", [])
    merged = " ".join(summaries)
    state["merged_summary"] = merged
    return state


def refine_summary_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    summary = state.get("merged_summary", "")
    limit = state.get("summary_limit", 300)

    refined = summary[:limit]
    state["final_summary"] = refined
    state["summary_length"] = len(refined)

    # if still too long, keep looping
    if len(refined) > limit:
        state["keep_looping"] = "yes"
    else:
        state["keep_looping"] = "no"

    return state


def register_summarization_tools() -> None:
    registry.register("split_text", split_text_tool)
    registry.register("summarize_chunks", summarize_chunks_tool)
    registry.register("merge_summaries", merge_summaries_tool)
    registry.register("refine_summary", refine_summary_tool)
