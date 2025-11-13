import threading
from query_watch.core.query_record import QueryRecord


class QueryWatcher:
    def __init__(self, threshold_ms: float = 100.0) -> None:
        self.threshold_ms = threshold_ms
        self._queries: list[QueryRecord] = []
        self._lock = threading.Lock()

    def _record_query(self, query: QueryRecord) -> None:
        with self._lock:
            self._queries.append(query)

    def collect(self) -> list[QueryRecord]:
        with self._lock:
            return self._queries.copy()

    def clear(self) -> None:
        with self._lock:
            self._queries.clear()
