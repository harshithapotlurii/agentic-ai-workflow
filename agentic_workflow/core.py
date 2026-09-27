from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass
from typing import Literal

Knowledge = {"refund": "Refund requests are reviewed within five business days.", "shipping": "Standard shipping takes three to five business days."}
Queries = {"open_orders": "SELECT COUNT(*) FROM orders WHERE status = 'open'"}


@dataclass(frozen=True)
class Result:
    status: Literal["answered", "abstained", "tool_error"]
    tool: str | None
    answer: str
    evidence: str | None


class Workflow:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def run(self, question: str) -> dict:
        q = question.lower().strip()
        if not q or len(q) > 2000:
            return asdict(Result("abstained", None, "Provide a question under 2000 characters.", None))
        if "refund" in q:
            evidence = Knowledge["refund"]
            return asdict(Result("answered", "knowledge", evidence, "sample-policy:refund"))
        if "shipping" in q:
            evidence = Knowledge["shipping"]
            return asdict(Result("answered", "knowledge", evidence, "sample-policy:shipping"))
        if "order" in q and "open" in q:
            try:
                count = self.db.execute(Queries["open_orders"]).fetchone()[0]
            except sqlite3.Error:
                return asdict(Result("tool_error", "sql", "Order data is unavailable.", None))
            return asdict(Result("answered", "sql", f"There are {count} open orders.", "sample-db:open_orders"))
        return asdict(Result("abstained", None, "No approved tool can answer this question.", None))


def sample_database() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, status TEXT NOT NULL)")
    db.executemany("INSERT INTO orders (status) VALUES (?)", [("open",), ("closed",), ("open",)])
    return db
