"""Ingest handlers — one per container format."""
from savegame_editor.ingest.registry import HANDLERS, detect_handler

__all__ = ["HANDLERS", "detect_handler"]