"""Durable SQLite key/value persistence with transactional writes."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class PersistentStore:
    def __init__(self, database_path: str | Path):
        self.path = Path(database_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        self.connection.commit()

    def put(self, key: str, value: Any) -> None:
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
        with self.connection:
            self.connection.execute(
                "INSERT INTO state(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, encoded),
            )

    def get(self, key: str, default: Any = None) -> Any:
        row = self.connection.execute("SELECT value FROM state WHERE key=?", (key,)).fetchone()
        return default if row is None else json.loads(row[0])

    def delete(self, key: str) -> bool:
        with self.connection:
            cursor = self.connection.execute("DELETE FROM state WHERE key=?", (key,))
        return cursor.rowcount == 1

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "PersistentStore":
        return self

    def __exit__(self, *_args) -> None:
        self.close()
