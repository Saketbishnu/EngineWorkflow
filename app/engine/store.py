from typing import Dict, Any
from uuid import UUID
from .graph import Graph

# simple in-memory stores
graphs: Dict[UUID, Graph] = {}

# run_id -> info
runs: Dict[UUID, Dict[str, Any]] = {}
