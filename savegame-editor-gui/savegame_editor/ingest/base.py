"""Base contract every ingest handler must satisfy."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RawContainer:
    """Result of ingest: header KV + still-compressed payload bytes."""

    magic: bytes
    header: dict[str, object]
    payload: bytes
    source_path: Path
    compressed: bool


class BaseIngestHandler(ABC):
    """Sniff + read a save container without touching its inner tree."""

    name: str = "base"
    magics: tuple[bytes, ...] = ()

    @abstractmethod
    def sniff(self, head: bytes) -> bool:
        """Return True if `head` (first 64 bytes) matches this handler."""

    @abstractmethod
    def read(self, path: Path) -> RawContainer:
        """Read the container. Must enforce config.limits.MAX_HEADER_BYTES."""