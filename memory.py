from __future__ import annotations

import time
from typing import Any


class MemoryStore:
    """
    In-memory cache layer for TURNX AI Director V4.

    Used for:
    - temporary conversation memory
    - prompt context tracking
    - reducing database reads
    """

    def __init__(self, ttl: int = 3600) -> None:
        self.ttl = ttl
        self.store: dict[int, dict[str, Any]] = {}

    # ==========================================================
    # Internal helpers
    # ==========================================================

    def _is_expired(self, entry: dict[str, Any]) -> bool:
        return time.time() > entry["expires_at"]

    def _cleanup(self) -> None:
        now = time.time()
        to_delete = [
            k for k, v in self.store.items()
            if v["expires_at"] < now
        ]

        for k in to_delete:
            del self.store[k]

    # ==========================================================
    # Public API
    # ==========================================================

    def set(self, key: int, value: Any) -> None:
        self.store[key] = {
            "value": value,
            "expires_at": time.time() + self.ttl,
        }

    def get(self, key: int) -> Any | None:
        self._cleanup()

        entry = self.store.get(key)

        if not entry:
            return None

        if self._is_expired(entry):
            del self.store[key]
            return None

        return entry["value"]

    def delete(self, key: int) -> None:
        if key in self.store:
            del self.store[key]
