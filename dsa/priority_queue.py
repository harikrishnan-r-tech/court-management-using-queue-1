"""
Priority Queue Data Structure
==============================
Uses Python's heapq module (min-heap).
We negate priorities so that 'High' comes out first.

Priority encoding:
  High   -> heap key 0   (highest urgency)
  Medium -> heap key 1
  Low    -> heap key 2

Tie-breaking: filing date (earlier date = higher priority among ties).

Time Complexity:
  push -> O(log n)
  pop  -> O(log n)
  peek -> O(1)
"""

import heapq


# Map priority labels to integer keys (lower int = higher priority in min-heap)
_PRIORITY_MAP = {"High": 0, "Medium": 1, "Low": 2}


class PriorityQueue:
    """Min-heap backed priority queue for court cases."""

    def __init__(self):
        # heap stores tuples: (priority_key, filing_date_str, case_dict)
        # heapq always pops the smallest tuple first.
        self._heap = []
        self._counter = 0  # secondary tie-breaker to avoid comparing dicts

    def push(self, case):
        """Insert a case into the priority queue.  O(log n)"""
        priority_key = _PRIORITY_MAP.get(case.get("priority", "Low"), 2)
        filing_date = case.get("filing_date", "9999-12-31")  # earlier = better
        # Use a counter as a third key so we never compare two dicts
        heapq.heappush(self._heap, (priority_key, filing_date, self._counter, case))
        self._counter += 1

    def pop(self):
        """Remove and return the highest-priority case.  O(log n)"""
        if self.is_empty():
            return None
        _, _, _, case = heapq.heappop(self._heap)
        return case

    def peek(self):
        """Return (without removing) the highest-priority case.  O(1)"""
        if self.is_empty():
            return None
        _, _, _, case = self._heap[0]
        return case

    def display(self):
        """
        Return all cases sorted by priority order.
        We sort a COPY of the heap so the actual heap is unchanged.  O(n log n)
        """
        sorted_items = sorted(self._heap, key=lambda x: (x[0], x[1]))
        return [item[3] for item in sorted_items]

    def is_empty(self):
        return len(self._heap) == 0

    def size(self):
        return len(self._heap)
