"""Pre-encode sanity checks. Catches what the GUI can't."""
from __future__ import annotations

from dataclasses import dataclass

from savegame_editor.config.limits import MAX_NODES_PER_TREE
from savegame_editor.models.save_tree import SaveTree


@dataclass(slots=True)
class ValidationReport:
    ok: bool
    errors: list[str]
    warnings: list[str]


def validate(tree: SaveTree) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []

    if len(tree.nodes) > MAX_NODES_PER_TREE:
        errors.append(f"node count {len(tree.nodes)} exceeds {MAX_NODES_PER_TREE}")

    for path, node in tree.nodes.items():
        if not path:
            errors.append("empty node path")
        if node.type_tag == "int32" and isinstance(node.value, int):
            if not (-2**31 <= node.value < 2**31):
                errors.append(f"{path}: int32 overflow ({node.value})")
        if node.type_tag == "str" and isinstance(node.value, str):
            if len(node.value.encode("utf-8")) > 64 * 1024:
                warnings.append(f"{path}: very long string ({len(node.value)} chars)")

    return ValidationReport(ok=not errors, errors=errors, warnings=warnings)