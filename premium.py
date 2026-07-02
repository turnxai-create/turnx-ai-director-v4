# premium.py
# TURNX AI Director V4 - Premium Access System

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta


class PremiumSystem:
    def __init__(self, db_path: str = "turnx.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            plan TEXT DEFAULT 'free',
            usage_count INTEGER DEFAULT 0,
            last_reset TEXT
        )
        """)

        conn.commit()
        conn.close()

    def is_premium(self, chat_id: int) -> bool:
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute("SELECT plan FROM users WHERE chat_id=?", (chat_id,))
        row = cursor.fetchone()

        conn.close()

        return row is not None and row[0] == "premium"

    def require_access(self, chat_id: int):
        """
        Returns None if allowed, otherwise returns error message.
        """
        if self.is_premium(chat_id):
            return None

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT usage_count FROM users WHERE chat_id=?",
            (chat_id,)
        )

        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO users (chat_id, plan, usage_count, last_reset) VALUES (?, 'free', 0, ?)",
                (chat_id, datetime.utcnow().isoformat())
            )
            conn.commit()
            conn.close()
            return None

        usage = row[0]

        if usage >= 10:
            conn.close()
            return "⚠️ Free limit reached. Upgrade to premium."

        conn.close()
        return None

    def increment_usage(self, chat_id: int):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT usage_count FROM users WHERE chat_id=?",
            (chat_id,)
        )

        row = cursor.fetchone()

        if row is None:
            cursor.execute(
                "INSERT INTO users (chat_id, usage_count, last_reset) VALUES (?, 1, ?)",
                (chat_id, datetime.utcnow().isoformat())
            )
        else:
            cursor.execute(
                "UPDATE users SET usage_count = usage_count + 1 WHERE chat_id=?",
                (chat_id,)
            )

        conn.commit()
        conn.close()


# Singleton instance used across project
premium = PremiumSystem()quests"] += 1
