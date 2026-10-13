"""Decode RawContainer -> SaveTree. Decompression + tree walk live here."""
from __future__ import annotations

import zlib

import lz4.block
import zstandard as zstd

from savegame_editor.config.limits import MAX_DECOMPRESSED_BYTES
from savegame_editor.ingest.base import RawContainer
from savegame_editor.models.save_tree import SaveNode, SaveTree
from savegame_editor.utils.binary_reader import BinaryReader


def _decompress(container: RawContainer) -> bytes:
    payload = container.payload
    if not container.compressed:
        return payload
    if len(payload) > MAX_DECOMPRESSED_BYTES:
        raise ValueError("compressed payload exceeds ceiling")
    try:
        out = zlib.decompress(payload)
    except zlib.error:
        # Fall back to zstd for UE5 builds that swapped the codec.
        out = zstd.ZstdDecompressor().decompress(payload, max_output_size=MAX_DECOMPRESSED_BYTES)
    if len(out) > MAX_DECOMPRESSED_BYTES:
        raise ValueError("decompressed tree exceeds ceiling")
    return out


def decode(container: RawContainer) -> SaveTree:
    """Produce a SaveTree. Offsets are byte offsets into the decoded payload."""
    body = _decompress(container)
    engine = "unreal" if container.magic == b"GVAS" else "unity"
    tree = SaveTree(container_format=engine, engine=engine, meta=dict(container.header))
    r = BinaryReader(body)
    node_count = 0
    while r.remaining() > 0 and node_count < 250_000:
        try:
            path = r.fstring()
        except EOFError:
            break
        if not path:
            continue
        type_tag = r.u8()
        offset = r.tell()
        value = r.read_typed(type_tag)
        tree.nodes[path] = SaveNode(path=path, value=value, type_tag=_tag_name(type_tag), offset=offset)
        node_count += 1
    return tree


_TAGS = {0: "int32", 1: "float", 2: "str", 3: "bool", 4: "int64"}


def _tag_name(tag: int) -> str:
    return _TAGS.get(tag, f"unknown_{tag}")