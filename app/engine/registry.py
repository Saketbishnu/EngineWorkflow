from typing import Callable, Dict, Any

ToolFn = Callable[[Dict[str, Any]], Dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolFn] = {}

    def register(self, name: str, fn: ToolFn) -> None:
        self._tools[name] = fn

    def get(self, name: str) -> ToolFn:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]


registry = ToolRegistry()
