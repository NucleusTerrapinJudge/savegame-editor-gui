"""Patch operation records emitted by the GUI, consumed by the patcher."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class PatchKind(str, Enum):
    SET_INT = "set_int"
    SET_FLOAT = "set_float"
    SET_STR = "set_str"
    UNLOCK = "unlock"
    DELETE = "delete"


class PatchOp(BaseModel):
    """A single, replayable edit. Kept immutable once queued."""

    kind: PatchKind
    path: str
    value: int | float | str | None = None
    source: str = Field(default="gui", description="gui | script | cli")

    model_config = {"frozen": True}