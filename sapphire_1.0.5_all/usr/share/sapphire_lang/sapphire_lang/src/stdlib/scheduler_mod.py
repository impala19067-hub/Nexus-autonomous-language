"""Durable and in-process scheduling primitives for Sapphire programs."""
import json
import sqlite3
import time
import threading
import uuid
from pathlib import Path

class SchedulerModule:
    @classmethod
    def schedule(cls, callback_fn, run_at: float, database_path: str = "sapphire_scheduler.sqlite", **kwargs):
        job_id = str(uuid.uuid4())
        path = Path(database_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(path)
        try:
            connection.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, run_at REAL NOT NULL, payload TEXT NOT NULL, status TEXT NOT NULL)")
            connection.execute("INSERT INTO jobs VALUES (?, ?, ?, 'pending')", (job_id, float(run_at), json.dumps(kwargs, sort_keys=True)))
            connection.commit()
        finally:
            connection.close()

        def _target():
            time.sleep(max(0.0, float(run_at) - time.time()))
            connection = sqlite3.connect(path)
            try:
                connection.execute("UPDATE jobs SET status='running' WHERE id=?", (job_id,))
                connection.commit()
            finally:
                connection.close()
            try:
                callback_fn(**kwargs)
            finally:
                connection = sqlite3.connect(path)
                try:
                    connection.execute("UPDATE jobs SET status='completed' WHERE id=?", (job_id,))
                    connection.commit()
                finally:
                    connection.close()

        threading.Thread(target=_target, daemon=True).start()
        return job_id

    @classmethod
    def resume(cls, job_id: str, callback_fn, database_path: str = "sapphire_scheduler.sqlite"):
        path = Path(database_path)
        connection = sqlite3.connect(path)
        try:
            row = connection.execute("SELECT run_at, payload, status FROM jobs WHERE id=?", (job_id,)).fetchone()
        finally:
            connection.close()
        if row is None:
            raise KeyError(f"Unknown scheduler job: {job_id}")
        if row[2] == "completed":
            return False
        cls.schedule(callback_fn, row[0], database_path, **json.loads(row[1]))
        return True

    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)

    @staticmethod
    def delay(ms: int):
        time.sleep(ms / 1000.0)

    @staticmethod
    def run_later(seconds: float, callback_fn):
        def _target():
            time.sleep(seconds)
            callback_fn()
        t = threading.Thread(target=_target, daemon=True)
        t.start()
        return t
