from __future__ import annotations

import sqlite3
import threading
from typing import Any, Optional


class Database:
    """
    Lightweight SQLite wrapper for TURNX AI Director V4.

    Stores:
    - user sessions
    - usage logs
    - model selections
    """

    def __init__(self, db_path: str = "turnx.db") -> None:
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()

    # ==========================================================
    # Core Connection
    # ==========================================================

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_state (
                    chat_id INTEGER PRIMARY KEY,
                    mode TEXT,
                    model TEXT
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    mode TEXT,
                    model TEXT,
                    prompt TEXT,
                    response TEXT
                )
                """
            )

            conn.commit()

    # ==========================================================
    # User State
    # ==========================================================

    def set_state(self, chat_id: int, mode: str, model: str) -> None:
        with self.lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_state(chat_id, mode, model)
                VALUES (?, ?, ?)
                ON CONFLICT(chat_id)
                DO UPDATE SET mode=excluded.mode, model=excluded.model
                """,
                (chat_id, mode, model),
            )
            conn.commit()

    def get_state(self, chat_id: int) -> Optional[dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_state WHERE chat_id=?",
                (chat_id,),
            ).fetchone()

            return dict(row) if row else None
from __future__ import annotations

import sqlite3
import threading
from typing import Any, Optional


class Database:
    """
    Lightweight SQLite wrapper for TURNX AI Director V4.

    Stores:
    - user sessions
    - usage logs
    - model selections
    """

    def __init__(self, db_path: str = "turnx.db") -> None:
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()

    # ==========================================================
    # Core Connection
    # ==========================================================

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_state (
                    chat_id INTEGER PRIMARY KEY,
                    mode TEXT,
                    model TEXT
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    mode TEXT,
                    model TEXT,
                    prompt TEXT,
                    response TEXT
                )
                """
            )

            conn.commit()

    # ==========================================================
    # User State
    # ==========================================================

    def set_state(self, chat_id: int, mode: str, model: str) -> None:
        with self.lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_state(chat_id, mode, model)
                VALUES (?, ?, ?)
                ON CONFLICT(chat_id)
                DO UPDATE SET mode=excluded.mode, model=excluded.model
                """,
                (chat_id, mode, model),
            )
            conn.commit()

    def get_state(self, chat_id: int) -> Optional[dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_state WHERE chat_id=?",
                (chat_id,),
            ).fetchone()

            return dict(row) if row else None
