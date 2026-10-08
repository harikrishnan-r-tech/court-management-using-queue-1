"""
Stack Data Structure
====================
A Stack follows LIFO (Last-In, First-Out) order.
Completed cases are pushed onto the stack; the most recently
completed case is always on top.

Time Complexity:
  push   -> O(1)
  pop    -> O(1)
  peek   -> O(1)
  display-> O(n)
"""


class CaseStack:
    """LIFO Stack implemented with a Python list."""

    def __init__(self):
        # Top of stack = last element in the list
        self._data = []

    # ------------------------------------------------------------------
    # push: Place a completed case on TOP of the stack  O(1)
    # ------------------------------------------------------------------
    def push(self, case):
        """Push a case onto the top of the stack."""
        self._data.append(case)

    # ------------------------------------------------------------------
    # pop: Remove the TOP (most-recently completed) case  O(1)
    # ------------------------------------------------------------------
    def pop(self):
        """Remove and return the top case, or None if empty."""
        if self.is_empty():
            return None
        return self._data.pop()

    # ------------------------------------------------------------------
    # peek: Look at the TOP case without removing it  O(1)
    # ------------------------------------------------------------------
    def peek(self):
        """Return (but do not remove) the top case, or None if empty."""
        if self.is_empty():
            return None
        return self._data[-1]

    # ------------------------------------------------------------------
    # display: Return cases in stack order (top first)  O(n)
    # ------------------------------------------------------------------
    def display(self):
        """Return list of cases with the TOP (most recent) first."""
        return list(reversed(self._data))

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)
