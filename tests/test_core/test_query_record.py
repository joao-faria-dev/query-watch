from datetime import datetime
from query_watch.core.query_record import QueryRecord


def test_query_record_creation():
    record = QueryRecord(
        sql="SELECT * FROM users",
        duration_ms=123.45,
        timestamp=datetime(2025, 11, 12, 12, 0, 0),
    )

    assert record.sql == "SELECT * FROM users"
    assert record.duration_ms == 123.45
    assert record.timestamp == datetime(2025, 11, 12, 12, 0, 0)
    assert record.rows is None
    assert record.stack_trace is None
    assert record.normnalized_sql is None
