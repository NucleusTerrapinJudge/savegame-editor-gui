"""EditorService — the single façade the GUI talks to. Owns the pipeline."""
from __future__ import annotations

from pathlib import Path

from loguru import logger

from savegame_editor.config.settings import Settings
from savegame_editor.ingest.registry import ingest
from savegame_editor.models.patch_op import PatchOp
from savegame_editor.models.save_tree import SaveTree
from savegame_editor.output.atomic_writer import atomic_write
from savegame_editor.processors.decoder import decode
from savegame_editor.processors.encoder import encode, header_bytes
from savegame_editor.processors.patcher import apply_patches
from savegame_editor.processors.validator import validate
from savegame_editor.utils.worker_pool import WorkerPool


class EditorService:
    """Stateless-per-call orchestration. The GUI holds one of these."""

    def __init__(self, pool: WorkerPool, settings: Settings) -> None:
        self._pool = pool
        self._settings = settings
        self._loaded: dict[Path, SaveTree] = {}

    def load(self, path: Path) -> SaveTree:
        container = ingest(path)
        tree = decode(container)
        self._loaded[path] = tree
        logger.info("loaded {} ({} nodes, engine={})", path.name, len(tree.nodes), tree.engine)
        return tree

    def apply(self, path: Path, ops: list[PatchOp]) -> SaveTree:
        tree = self._loaded.get(path) or self.load(path)
        apply_patches(tree, ops)
        report = validate(tree)
        if not report.ok:
            raise ValueError("validation failed: " + "; ".join(report.errors))
        for w in report.warnings:
            logger.warning("validate: {}", w)
        return tree

    def save(self, path: Path, *, backup: bool = True) -> Path:
        tree = self._loaded[path]
        payload = encode(tree, compress=(tree.engine == "unreal"))
        full = header_bytes(tree) + payload
        written = atomic_write(path, full, backup=backup)
        logger.info("wrote {} ({} bytes)", written.name, len(full))
        return written

    def export_json(self, path: Path, dest: Path) -> Path:
        import json
        tree = self._loaded[path]
        dest_resolved = dest.resolve()
        if not str(dest_resolved).startswith(str(self._settings.export_root.resolve())):
            raise PermissionError("export path outside configured export_root")
        dest_resolved.write_text(
            json.dumps({p: n.value for p, n in tree.nodes.items()}, indent=2),
            encoding="utf-8",
        )
        return dest_resolved