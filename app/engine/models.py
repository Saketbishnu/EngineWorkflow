from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel


class NodeSpec(BaseModel):
    id: str                  # unique node id
    tool: str                # tool/function name from registry
    next: Optional[str] = None   # default next node id
    branch_on: Optional[str] = None       # key in state to inspect
    branches: Optional[Dict[str, Optional[str]]] = None
    # example: {"yes": "split", "no": null}


class GraphCreateRequest(BaseModel):
    nodes: List[NodeSpec]
    start_node: str


class GraphCreateResponse(BaseModel):
    graph_id: UUID


class RunRequest(BaseModel):
    graph_id: UUID
    initial_state: Dict[str, Any]


class NodeLog(BaseModel):
    node_id: str
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    status: str


class RunResponse(BaseModel):
    run_id: UUID
    final_state: Dict[str, Any]
    log: List[NodeLog]


class RunStateResponse(BaseModel):
    run_id: UUID
    current_state: Dict[str, Any]
    status: str
    log: List[NodeLog]
