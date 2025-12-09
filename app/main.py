from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from typing import Dict, Any

from .engine.models import (
    GraphCreateRequest,
    GraphCreateResponse,
    RunRequest,
    RunResponse,
    RunStateResponse,
    NodeSpec,
)
from .engine.graph import Graph, Node
from .engine import store
from .workflows.summarization import register_summarization_tools


app = FastAPI(
    title="Mini Agent Workflow Engine",
    description="Simple workflow/graph engine for AI Engineering Internship assignment",
)


@app.on_event("startup")
def startup_event() -> None:
    # register our tools when app boots
    register_summarization_tools()


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(req: GraphCreateRequest) -> GraphCreateResponse:
    graph_id = uuid4()
    nodes_dict: Dict[str, Node] = {spec.id: Node(spec) for spec in req.nodes}
    graph = Graph(graph_id=graph_id, nodes=nodes_dict, start_node=req.start_node)
    store.graphs[graph_id] = graph
    return GraphCreateResponse(graph_id=graph_id)


@app.post("/graph/run", response_model=RunResponse)
async def run_graph(req: RunRequest) -> RunResponse:
    graph = store.graphs.get(req.graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    run_id = uuid4()
    final_state, logs = graph.run(req.initial_state)
    store.runs[run_id] = {
        "graph_id": req.graph_id,
        "state": final_state,
        "log": [log.dict() for log in logs],
        "status": "finished",
    }

    return RunResponse(
        run_id=run_id,
        final_state=final_state,
        log=logs,
    )


@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
async def get_run_state(run_id: UUID) -> RunStateResponse:
    run = store.runs.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunStateResponse(
        run_id=run_id,
        current_state=run["state"],
        status=run["status"],
        log=run["log"],
    )


# Optional helper: create the example summarization graph with one call
@app.post("/graph/example/summarization", response_model=GraphCreateResponse)
async def create_example_summarization_graph() -> GraphCreateResponse:
    """
    Convenience endpoint to create Option B: Summarization + Refinement workflow.
    """
    node_specs = [
        NodeSpec(
            id="split",
            tool="split_text",
            next="summarize",
        ),
        NodeSpec(
            id="summarize",
            tool="summarize_chunks",
            next="merge",
        ),
        NodeSpec(
            id="merge",
            tool="merge_summaries",
            next="refine",
        ),
        NodeSpec(
            id="refine",
            tool="refine_summary",
            branch_on="keep_looping",
            branches={
                "yes": "split",   # loop back
                "no": None        # stop
            },
        ),
    ]
    req = GraphCreateRequest(start_node="split", nodes=node_specs)
    return await create_graph(req)
