from dataclasses import dataclass
from datetime import datetime


@dataclass
class QueryRecord:
    sql: str
    duration_ms: float
    timestamp: datetime
    rows: int | None = None
    normnalized_sql: str | None = None
    stack_trace: list[str] | None = None
