"""Local retrieval-augmented memory using SQLite FTS5."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class SemanticMemory:
    """Durable document memory with ranked full-text retrieval and context assembly."""

    def __init__(self, database_path: str | Path):
        self.connection = sqlite3.connect(database_path)
        self.connection.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS documents USING fts5(" 
            "key UNINDEXED, content, metadata UNINDEXED)"
        )

    def remember(self, key: str, content: str, metadata: str = "") -> None:
        self.forget(key)
        self.connection.execute(
            "INSERT INTO documents(key, content, metadata) VALUES(?, ?, ?)",
            (key, content, metadata),
        )
        self.connection.commit()

    def forget(self, key: str) -> None:
        self.connection.execute("DELETE FROM documents WHERE key=?", (key,))
        self.connection.commit()

    def retrieve(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        rows = self.connection.execute(
            "SELECT key, content, metadata, rank FROM documents "
            "WHERE documents MATCH ? ORDER BY rank LIMIT ?",
            (query, limit),
        ).fetchall()
        return [
            {"key": key, "content": content, "metadata": metadata, "rank": str(rank)}
            for key, content, metadata, rank in rows
        ]

    def context(self, query: str, limit: int = 5) -> str:
        return "\n\n".join(item["content"] for item in self.retrieve(query, limit))

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SemanticMemory":
        return self

    def __exit__(self, *_args) -> None:
        self.close()
