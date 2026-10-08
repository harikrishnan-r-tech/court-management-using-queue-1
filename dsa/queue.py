"""
Queue Data Structure
====================
A Queue follows FIFO (First-In, First-Out) order.
Cases are added to the back and heard (removed) from the front.
This models a real court hearing queue.

Time Complexity:
  enqueue  -> O(1)  (append to end of list)
  dequeue  -> O(n)  (pop(0) shifts all elements left)
  peek     -> O(1)  (read index 0)
  display  -> O(n)  (iterate all elements)
"""


class CaseQueue:
    """A simple Queue implemented with a Python list."""

    def __init__(self):
        # Internal list stores cases in order of arrival
        self._data = []

    # ------------------------------------------------------------------
    # enqueue: Add a case to the BACK of the queue  O(1)
    # ------------------------------------------------------------------
    def enqueue(self, case):
        """Add a case dict to the back of the queue."""
        self._data.append(case)

    # ------------------------------------------------------------------
    # dequeue: Remove the FRONT case (oldest) from the queue  O(n)
    # Python list.pop(0) is O(n) because it shifts every element.
    # A deque would give O(1) dequeue, but we use a list to keep the
    # code readable for teaching.
    # ------------------------------------------------------------------
    def dequeue(self):
        """Remove and return the front case, or None if empty."""
        if self.is_empty():
            return None
        return self._data.pop(0)

    # ------------------------------------------------------------------
    # peek: Look at the FRONT case without removing it  O(1)
    # ------------------------------------------------------------------
    def peek(self):
        """Return (but do not remove) the front case, or None if empty."""
        if self.is_empty():
            return None
        return self._data[0]

    # ------------------------------------------------------------------
    # display: Return a copy of all cases in queue order  O(n)
    # ------------------------------------------------------------------
    def display(self):
        """Return a list of all cases in FIFO order (front first)."""
        return list(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"CaseQueue({self._data})"
