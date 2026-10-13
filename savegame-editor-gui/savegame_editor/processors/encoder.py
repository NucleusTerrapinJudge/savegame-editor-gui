"""Serialize SaveTree -> bytes. Must round-trip with decoder.decode()."""
from __future__ import annotations

import struct
import zlib

from savegame_editor.models.save_tree import SaveTree
from savegame_editor.utils.binary_writer import BinaryWriter

_TYPE_BY_TAG = {"int32": 0, "float": 1, "str": 2, "bool": 3, "int64": 4}


def encode(tree: SaveTree, *, compress: bool = True) -> bytes:
    """Emit the payload (post-header). GVAS header is re-emitted by the driver."""
    w = BinaryWriter()
    for node in tree.ordered():
        w.fstring(node.path)
        w.u8(_TYPE_BY_TAG.get(node.type_tag, 0))
        w.write_typed(node.value, node.type_tag)
    body = w.bytes()
    if not compress:
        return body
    return zlib.compress(body, level=6)


def header_bytes(tree: SaveTree) -> bytes:
    """Reconstruct the container header for GVAS saves."""
    if tree.engine != "unreal":
        return b""
    meta = tree.meta
    out = bytearray()
    out += b"GVAS"
    out += struct.pack("<I", int(meta.get("save_version", 2)))
    out += struct.pack("<I", int(meta.get("package_version", 522)))
    engine = str(meta.get("engine", "4.27.0")).split(".")
    while len(engine) < 3:
        engine.append("0")
    out += struct.pack("<HHH", int(engine[0]), int(engine[1]), int(engine[2]))
    build = str(meta.get("build", "")).encode("utf-8") + b"\x00"
    out += struct.pack("<I", len(build)) + build
    custom = meta.get("custom", {}) or {}
    out += struct.pack("<I", len(custom))
    for k, v in custom.items():
        kb = str(k).encode("utf-8") + b"\x00"
        vb = str(v).encode("utf-8") + b"\x00"
        out += struct.pack("<I", len(kb)) + kb + struct.pack("<I", len(vb)) + vb
    return bytes(out)