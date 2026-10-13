"""Logical save tree — the in-memory object every processor mutates."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SaveNode:
    """One addressable value in a save. `path` is dotted, e.g. `player.stats.gold`."""

    path: str
    value: Any
    type_tag: str = "int32"
    offset: int = -1  # byte offset in the decoded payload, -1 if synthetic


@dataclass(slots=True)
class SaveTree:
    """Flat index over a decoded save. Ordered by `offset` for re-encode."""

    container_format: str
    engine: str
    nodes: dict[str, SaveNode] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)

    def get(self, path: str) -> SaveNode | None:
        return self.nodes.get(path)

    def set(self, path: str, value: Any) -> None:
        node = self.nodes.get(path)
        if node is None:
            self.nodes[path] = SaveNode(path=path, value=value, type_tag="int32")
        else:
            node.value = value

    def ordered(self) -> list[SaveNode]:
        return sorted(self.nodes.values(), key=lambda n: n.offset)