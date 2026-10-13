"""Atomic write with backup. A crash mid-write must never brick a save."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from loguru import logger


def atomic_write(target: Path, data: bytes, *, backup: bool = True) -> Path:
    """Write `data` to `target` atomically. Keeps a `.bak` if requested.

    Uses write-tmp + fsync + os.replace so a power loss leaves either the
    old file or the new one, never a half-written one.
    """
    target = target.resolve()
    tmp = target.with_suffix(target.suffix + ".tmp")
    bak = target.with_suffix(target.suffix + ".bak")

    if backup and target.exists():
        shutil.copy2(target, bak)

    with tmp.open("wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())

    os.replace(tmp, target)
    _fsync_dir(target.parent)
    logger.debug("atomic_write: {} ({} bytes)", target.name, len(data))
    return target


def _fsync_dir(directory: Path) -> None:
    if os.name != "posix":
        return  # Windows lacks dir fsync; os.replace is atomic enough here.
    try:
        fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        pass