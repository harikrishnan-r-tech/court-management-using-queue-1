"""
Linked List Data Structure
===========================
Each case's hearing/action HISTORY is stored as a singly linked list.
Each node holds one history entry. Traversal goes from the FIRST action
to the LATEST, simulating a timeline.

Time Complexity:
  insert (at tail) -> O(n)  (must traverse to find tail)
  delete           -> O(n)  (must find node by value)
  display          -> O(n)
"""


class Node:
    """A single node in the linked list."""

    def __init__(self, data):
        self.data = data        # dict: {entry_id, action, date, note}
        self.next = None        # pointer to next Node


class LinkedList:
    """Singly linked list to track case history."""

    def __init__(self):
        self.head = None  # first node (oldest history entry)

    # ------------------------------------------------------------------
    # insert: Add a new history entry at the TAIL  O(n)
    # Tail insertion keeps entries in chronological order.
    # ------------------------------------------------------------------
    def insert(self, data):
        """Append a history entry dict to the end of the list."""
        new_node = Node(data)
        if self.head is None:
            # List is empty, new node becomes the head
            self.head = new_node
            return
        # Walk to the last node
        current = self.head
        while current.next is not None:
            current = current.next
        # Link the last node to our new node
        current.next = new_node

    # ------------------------------------------------------------------
    # delete: Remove a node by entry_id  O(n)
    # ------------------------------------------------------------------
    def delete(self, entry_id):
        """
        Remove the node whose data['entry_id'] matches entry_id.
        Returns True if deleted, False if not found.
        """
        if self.head is None:
            return False

        # Special case: the head node is the one to delete
        if self.head.data.get("entry_id") == entry_id:
            self.head = self.head.next
            return True

        # Walk the list looking for the node just BEFORE the target
        current = self.head
        while current.next is not None:
            if current.next.data.get("entry_id") == entry_id:
                # Bypass the target node
                current.next = current.next.next
                return True
            current = current.next

        return False  # not found

    # ------------------------------------------------------------------
    # display: Return all history entries as a list  O(n)
    # ------------------------------------------------------------------
    def display(self):
        """Traverse the list and return all data dicts in order."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self.head is None

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
