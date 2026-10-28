"""
Cache implementation requiring behavior-preserving refactoring.
"""
import time
from typing import Any, Optional, Dict, List, Tuple

class SimpleLRUCache:
    """
    Naive linear-scan LRU cache implementation.
    Goal: Refactor to O(1) operations while preserving 100% of behavioral invariants and API contracts.
    """
    def __init__(self, capacity: int = 100):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        # Stored as list of [key, val, last_accessed_time]
        self._entries: List[List[Any]] = []
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def get(self, key: str) -> Optional[Any]:
        for entry in self._entries:
            if entry[0] == key:
                entry[2] = time.time()
                self._hits += 1
                return entry[1]
        self._misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        # Check if key exists
        for entry in self._entries:
            if entry[0] == key:
                entry[1] = value
                entry[2] = time.time()
                return

        # Check capacity
        if len(self._entries) >= self.capacity:
            # Find oldest
            oldest_idx = 0
            oldest_time = self._entries[0][2]
            for i in range(1, len(self._entries)):
                if self._entries[i][2] < oldest_time:
                    oldest_time = self._entries[i][2]
                    oldest_idx = i
            self._entries.pop(oldest_idx)
            self._evictions += 1

        self._entries.append([key, value, time.time()])

    def evict(self, key: str) -> bool:
        for i, entry in enumerate(self._entries):
            if entry[0] == key:
                self._entries.pop(i)
                return True
        return False

    def size(self) -> int:
        return len(self._entries)

    def stats(self) -> Dict[str, int]:
        return {
            "hits": self._hits,
            "misses": self._misses,
            "evictions": self._evictions,
            "size": len(self._entries),
            "capacity": self.capacity
        }
