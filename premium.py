from __future__ import annotations

import time
from typing import Dict, Optional


class PremiumManager:
    """
    Simple premium access control for TURNX AI Director V4.

    Controls:
    - feature access
    - usage limits
    - subscription state (basic structure only)
    """

    def __init__(self) -> None:
        self.users: Dict[int, dict] = {}

    # ==========================================================
    # User Registration
    # ==========================================================

    def register_user(self, chat_id: int) -> None:
        if chat_id not in self.users:
            self.users[chat_id] = {
                "premium": False,
                "requests": 0,
                "reset_at": time.time() + 86400,  # daily reset
            }

    # ==========================================================
    # Access Check
    # ==========================================================

    def is_premium(self, chat_id: int) -> bool:
        self.register_user(chat_id)
        return self.users[chat_id]["premium"]

    # ==========================================================
    # Usage Tracking
    # ==========================================================

    def can_use(self, chat_id: int, limit: int = 10) -> bool:
        self.register_user(chat_id)

        user = self.users[chat_id]

        # reset daily quota
        if time.time() > user["reset_at"]:
            user["requests"] = 0
            user["reset_at"] = time.time() + 86400

        return user["requests"] < limit

    def increment_usage(self, chat_id: int) -> None:
        self.register_user(chat_id)
        self.users[chat_id]["requests"] += 1
from __future__ import annotations

import time
from typing import Dict, Optional


class PremiumManager:
    """
    Simple premium access control for TURNX AI Director V4.

    Controls:
    - feature access
    - usage limits
    - subscription state (basic structure only)
    """

    def __init__(self) -> None:
        self.users: Dict[int, dict] = {}

    # ==========================================================
    # User Registration
    # ==========================================================

    def register_user(self, chat_id: int) -> None:
        if chat_id not in self.users:
            self.users[chat_id] = {
                "premium": False,
                "requests": 0,
                "reset_at": time.time() + 86400,  # daily reset
            }

    # ==========================================================
    # Access Check
    # ==========================================================

    def is_premium(self, chat_id: int) -> bool:
        self.register_user(chat_id)
        return self.users[chat_id]["premium"]

    # ==========================================================
    # Usage Tracking
    # ==========================================================

    def can_use(self, chat_id: int, limit: int = 10) -> bool:
        self.register_user(chat_id)

        user = self.users[chat_id]

        # reset daily quota
        if time.time() > user["reset_at"]:
            user["requests"] = 0
            user["reset_at"] = time.time() + 86400

        return user["requests"] < limit

    def increment_usage(self, chat_id: int) -> None:
        self.register_user(chat_id)
        self.users[chat_id]["requests"] += 1
