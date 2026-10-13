"""Hard limits enforced by every ingest handler. DoS-proofing lives here."""
from __future__ import annotations

MAX_FIELD_BYTES = 64 * 1024 * 1024          # single string/blob field cap
MAX_HEADER_BYTES = 1 * 1024 * 1024          # container header cap
MAX_NODES_PER_TREE = 250_000                # guards cyclic struct expansion
MAX_DECOMPRESSED_BYTES = 512 * 1024 * 1024  # zstd/lz4 bomb ceiling
ALLOWED_EXPORT_SUFFIXES = frozenset({".json", ".sav.json", ".txt"})