"""Little-endian binary reader with bounds checks. Used by all handlers."""
from __future__ import annotations

import struct


class BinaryReader:
    """Cursors over an immutable buffer. Raises EOFError past the end."""

    __slots__ = ("_buf", "_pos")

    def __init__(self, buf: bytes) -> None:
        self._buf = buf
        self._pos = 0

    def tell(self) -> int:
        return self._pos

    def remaining(self) -> int:
        return len(self._buf) - self._pos

    def read(self, n: int) -> bytes:
        if self._pos + n > len(self._buf):
            raise EOFError(f"read {n} at {self._pos} exceeds {len(self._buf)}")
        out = self._buf[self._pos:self._pos + n]
        self._pos += n
        return out

    def u8(self) -> int:
        return self.read(1)[0]

    def u16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def u32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def i32(self