from __future__ import annotations

import hashlib
import json
from typing import Any


class CharacterLock:
    """
    Ensures consistent AI character generation across images/videos.

    This locks:
    - facial structure
    - identity signature
    - style consistency hash
    """

    def __init__(self) -> None:
        self.cache: dict[str, dict[str, Any]] = {}

    # ==========================================================
    # Core Identity Lock
    # ==========================================================

    def generate_lock(self, prompt: str) -> str:
        """
        Creates a deterministic identity hash from prompt.
        """

        normalized = self._normalize(prompt)
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _normalize(self, prompt: str) -> str:
        return " ".join(prompt.lower().strip().split())

    # ==========================================================
    # Store / Retrieve Character Data
    # ==========================================================

    def store_character(self, prompt: str, data: dict[str, Any]) -> str:
        lock_id = self.generate_lock(prompt)

        self.cache[lock_id] = {
            "prompt": prompt,
            "data": data,
        }

        return lock_id

    def get_character(self, lock_id: str) -> dict[str, Any] | None:
        return self.cache.get(lock_id)
from __future__ import annotations

import hashlib
import json
from typing import Any


class CharacterLock:
    """
    Ensures consistent AI character generation across images/videos.

    This locks:
    - facial structure
    - identity signature
    - style consistency hash
    """

    def __init__(self) -> None:
        self.cache: dict[str, dict[str, Any]] = {}

    # ==========================================================
    # Core Identity Lock
    # ==========================================================

    def generate_lock(self, prompt: str) -> str:
        """
        Creates a deterministic identity hash from prompt.
        """

        normalized = self._normalize(prompt)
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _normalize(self, prompt: str) -> str:
        return " ".join(prompt.lower().strip().split())

    # ==========================================================
    # Store / Retrieve Character Data
    # ==========================================================

    def store_character(self, prompt: str, data: dict[str, Any]) -> str:
        lock_id = self.generate_lock(prompt)

        self.cache[lock_id] = {
            "prompt": prompt,
            "data": data,
        }

        return lock_id

    def get_character(self, lock_id: str) -> dict[str, Any] | None:
        return self.cache.get(lock_id)
