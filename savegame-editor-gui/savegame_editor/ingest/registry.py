"""Handler registry — ordered by sniff specificity."""
from __future__ import annotations

from pathlib import Path

from savegame_editor.ingest.base import BaseIngestHandler, RawContainer
from savegame_editor.ingest.gvas_handler import GvasHandler
from savegame_editor.ingest.unity_handler import UnityHandler

HANDLERS: tuple[BaseIngestHandler, ...] = (GvasHandler(), UnityHandler())


def detect_handler(path: Path) -> BaseIngestHandler:
    """Read the first 64 bytes and pick the first matching handler."""
    with path.open("rb") as fh:
        head = fh.read(64)
    for handler in HANDLERS:
        if handler.sniff(head):
            return handler
    raise ValueError(f"no ingest handler for {path.name}: magic={head[:8]!r}")


def ingest(path: Path) -> RawContainer:
    return detect_handler(path).read(path)