"""Unity PlayerPrefs / BinaryFormatter container handler."""
from __future__ import annotations

import struct
from pathlib import Path

from savegame_editor.ingest.base import BaseIngestHandler, RawContainer


class UnityHandler(BaseIngestHandler):
    """Handles Unity saves that start with the PlayerPrefs magic or a raw
    BinaryFormatter stream header."""

    name = "unity"
    magics = (b"UnityPrf", b"\x00\x01\x00\x00\x00\xff\xff\xff\xff")

    def sniff(self, head: bytes) -> bool:
        return any(head.startswith(m) for m in self.magics)

    def read(self, path: Path) -> RawContainer:
        raw = path.read_bytes()
        if raw.startswith(b"UnityPrf"):
            magic = raw[:8]
            payload = raw[8:]
            header = {"format": "playerprefs", "entry_hint": struct.unpack("<I", raw[8:12])[0]}
        else:
            magic = raw[:8]
            payload = raw[8:]
            header = {"format": "binaryformatter"}
        return RawContainer(magic, header, payload, path, compressed=False)