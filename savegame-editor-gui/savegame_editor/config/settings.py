"""Runtime settings, loaded from %APPDATA%/savegame-editor-gui/settings.json."""
from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel, Field


def _default_root() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / ".config")
    return Path(base) / "savegame-editor-gui"


class Settings(BaseModel):
    """User-facing tunables. Never stores absolute save paths."""

    config_root: Path = Field(default_factory=_default_root)
    log_level: str = "INFO"
    max_workers: int = 4
    max_field_bytes: int = 64 * 1024 * 1024
    backup_suffix: str = ".bak"
    export_root: Path = Field(default_factory=lambda: _default_root() / "exports")

    @property
    def log_path(self) -> Path:
        return self.config_root / "logs" / "editor.log"

    def ensure_dirs(self) -> None:
        for p in (self.config_root, self.log_path.parent, self.export_root):
            p.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    root = _default_root()
    cfg_file = root / "settings.json"
    if cfg_file.exists():
        try:
            data = json.loads(cfg_file.read_text(encoding="utf-8"))
            settings = Settings(**data)
        except (json.JSONDecodeError, ValueError):
            settings = Settings()
    else:
        settings = Settings()
    settings.ensure_dirs()
    return settings