"""Apply PatchOp records to a SaveTree. Pure function, no I/O."""
from __future__ import annotations

from savegame_editor.models.patch_op import PatchKind, PatchOp
from savegame_editor.models.save_tree import SaveTree


class PatchError(RuntimeError):
    """Raised when a patch targets a missing path or type-mismatches."""


def apply_patches(tree: SaveTree, ops: list[PatchOp]) -> SaveTree:
    """Apply in order. Later ops see earlier ops' effects."""
    for op in ops:
        _apply_one(tree, op)
    return tree


def _apply_one(tree: SaveTree, op: PatchOp) -> None:
    if op.kind is PatchKind.DELETE:
        tree.nodes.pop(op.path, None)
        return
    if op.kind is PatchKind.UNLOCK:
        tree.set(op.path, True)
        return
    node = tree.get(op.path)
    if node is None and op.kind is not PatchKind.UNLOCK:
        raise PatchError(f"path not found: {op.path}")
    if op.kind is PatchKind.SET_INT and not isinstance(op.value, int):
        raise PatchError(f"set_int requires int, got {type(op.value).__name__}")
    if op.kind is PatchKind.SET_FLOAT and not isinstance(op.value, (int, float)):
        raise PatchError("set_float requires numeric value")
    tree.set(op.path, op.value)