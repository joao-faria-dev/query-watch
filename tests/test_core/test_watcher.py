from datetime import datetime
import threading
from query_watch.core.query_record import QueryRecord
from query_watch.core.watcher import QueryWatcher


def test_query_watcher_initialization():
    watcher = QueryWatcher()
    assert watcher.threshold_ms == 100.0
    assert watcher.collect() == []

    watcher = QueryWatcher(threshold_ms=50.0)
    assert watcher.threshold_ms == 50.0


def test_record_query():
    watcher = QueryWatcher()
    record = QueryRecord(
        sql="SELECT * FROM users",
        duration_ms=123.45,
        timestamp=datetime(2025, 11, 12, 12, 0, 0),
    )

    watcher._record_query(record)
    collected = watcher.collect()

    assert len(collected) == 1
    assert collected[0] == record
    assert collected[0].sql == "SELECT * FROM users"


def test_clear():
    watcher = QueryWatcher()
    records = [
        QueryRecord(
            sql="SELECT * FROM users",
            duration_ms=50.0,
            timestamp=datetime(2025, 11, 12, 12, 0, 0),
        ),
        QueryRecord(
            sql="SELECT * FROM posts",
            duration_ms=75.0,
            timestamp=datetime(2025, 11, 12, 12, 0, 1),
        ),
    ]

    for record in records:
        watcher._record_query(record)

    assert len(watcher.collect()) == 2
    watcher.clear()
    assert len(watcher.collect()) == 0


def test_thread_safety():
    watcher = QueryWatcher()
    num_threads = 10
    queries_per_thread = 50

    def record_queries(thread_id: int) -> None:
        for i in range(queries_per_thread):
            record = QueryRecord(
                sql=f"SELECT * FROM table_{thread_id}_{i}",
                duration_ms=float(i),
                timestamp=datetime(2025, 11, 12, 12, 0, 0),
            )
            watcher._record_query(record)

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=record_queries, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    collected = watcher.collect()
    expected_count = num_threads * queries_per_thread
    assert len(collected) == expected_count

    sql_statements = [q.sql for q in collected]
    assert len(sql_statements) == len(set(sql_statements))
