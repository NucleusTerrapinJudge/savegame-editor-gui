"""Export/import save profiles (the patch recipe JSON) — not the save itself."""
from __future__ import annotations

import json
from pathlib import Path

from savegame_editor.models.patch_op import PatchOp


def dump_profile(ops: list[PatchOp], dest: Path) -> Path:
    payload = {"version": 1, "ops": [op.model_dump(mode="json") for op in ops]}
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return dest


def load_profile(src: Path) -> list[PatchOp]:
    data = json.loads(src.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError(f"unsupported profile version: {data.get('version')}")
    return [PatchOp(**op) for op in data["ops"]]