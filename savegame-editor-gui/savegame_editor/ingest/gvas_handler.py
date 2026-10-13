"""UE4/UE5 GVAS container handler (Unreal `SaveGame` files)."""
from __future__ import annotations

import struct
from pathlib import Path

from savegame_editor.config.limits import MAX_HEADER_BYTES
from savegame_editor.ingest.base import BaseIngestHandler, RawContainer
from savegame_editor.utils.binary_reader import BinaryReader


class GvasHandler(BaseIngestHandler):
    """Parses the GVAS header: magic, version, engine tag, custom KV."""

    name = "gvas"
    magics = (b"GVAS",)

    def sniff(self, head: bytes) -> bool:
        return head.startswith(b"GVAS")

    def read(self, path: Path) -> RawContainer:
        raw = path.read_bytes()
        if len(raw) > MAX_HEADER_BYTES * 64:
            raise ValueError(f"GVAS file too large: {len(raw)} bytes")
        r = BinaryReader(raw)
        magic = r.read(4)
        save_version = r.u32()
        package_version = r.u32()
        engine_major = r.u16()
        engine_minor = r.u16()
        engine_patch = r.u16()
        build = r.fstring()
        custom_count = r.u32()
        custom: dict[str, str] = {}
        for _ in range(min(custom_count, 64)):
            key = r.fstring()
            val = r.fstring()
            custom[key] = val
        header = {
            "save_version": save_version,
            "package_version": package_version,
            "engine": f"{engine_major}.{engine_minor}.{engine_patch}",
            "build": build,
            "custom": custom,
        }
        payload = raw[r.tell():]
        # GVAS payloads are typically zlib; flag it, decoder decides.
        compressed = payload[:2] == b"\x78\x9c"
        return RawContainer(magic, header, payload, path, compressed)