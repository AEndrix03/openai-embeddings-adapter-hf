from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
from pathlib import Path


def build_cache_key(
    model_id: str,
    inputs: list[str],
    normalize: bool,
    dimensions: int | None,
    task: str | None,
) -> str:
    payload = {
        "dimensions": dimensions,
        "inputs": inputs,
        "model_id": model_id,
        "normalize": normalize,
        "task": task,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class EmbeddingResponseCache:
    def __init__(self, db_path: str, max_entries: int):
        self.db_path = Path(db_path)
        self.max_entries = max_entries
        self._lock = threading.Lock()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA synchronous=NORMAL;")
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS embedding_cache (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                last_access INTEGER NOT NULL
            )
            """
        )
        self._conn.commit()

    def get(self, key: str) -> list[list[float]] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT value FROM embedding_cache WHERE key = ?",
                (key,),
            ).fetchone()
            if row is None:
                return None
            now = int(time.time())
            self._conn.execute(
                "UPDATE embedding_cache SET last_access = ? WHERE key = ?",
                (now, key),
            )
            self._conn.commit()
            return json.loads(row[0])

    def set(self, key: str, value: list[list[float]]) -> None:
        now = int(time.time())
        serialized = json.dumps(value, separators=(",", ":"))
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO embedding_cache(key, value, created_at, last_access)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key)
                DO UPDATE SET value = excluded.value, last_access = excluded.last_access
                """,
                (key, serialized, now, now),
            )
            self._prune_if_needed()
            self._conn.commit()

    def _prune_if_needed(self) -> None:
        row = self._conn.execute("SELECT COUNT(1) FROM embedding_cache").fetchone()
        if row is None:
            return
        count = int(row[0])
        overflow = count - self.max_entries
        if overflow <= 0:
            return
        self._conn.execute(
            """
            DELETE FROM embedding_cache
            WHERE key IN (
                SELECT key FROM embedding_cache
                ORDER BY last_access ASC
                LIMIT ?
            )
            """,
            (overflow,),
        )
