from typing import Dict, Any, List, Optional
from uuid import UUID
from .models import NodeSpec, NodeLog
from .registry import registry


class Node:
    def __init__(self, spec: NodeSpec) -> None:
        self.id = spec.id
        self.tool_name = spec.tool
        self.next = spec.next
        self.branch_on = spec.branch_on
        self.branches = spec.branches or {}

    def run(self, state: Dict[str, Any]) -> (Dict[str, Any], Optional[str]):
        tool_fn = registry.get(self.tool_name)

        # capture before
        new_state = tool_fn(dict(state))  # pass a copy or mutate directly
        # Decide next node
        next_node = self.next

        if self.branch_on:
            key = self.branch_on
            value = new_state.get(key)
            # convert to string for branches keys
            if value is not None:
                value_str = str(value)
                if value_str in self.branches:
                    next_node = self.branches[value_str]

        return new_state, next_node


class Graph:
    def __init__(self, graph_id: UUID, nodes: Dict[str, Node], start_node: str) -> None:
        self.id = graph_id
        self.nodes = nodes
        self.start_node = start_node

    def run(self, initial_state: Dict[str, Any]) -> (Dict[str, Any], List[NodeLog]):
        state = dict(initial_state)
        logs: List[NodeLog] = []
        current_id: Optional[str] = self.start_node

        max_steps = 100  # safety limit
        steps = 0

        while current_id is not None and steps < max_steps:
            node = self.nodes[current_id]
            before = dict(state)
            state, next_id = node.run(state)
            after = dict(state)

            logs.append(NodeLog(
                node_id=current_id,
                state_before=before,
                state_after=after,
                status="ok"
            ))

            current_id = next_id
            steps += 1

        return state, logs
