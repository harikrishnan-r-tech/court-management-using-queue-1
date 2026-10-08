"""
Searching Algorithms
=====================
Three search strategies for finding cases:

1. Linear Search  O(n)   – scan every case one by one
2. Binary Search  O(log n) – requires a SORTED list by Case ID
3. Dictionary / Hash Lookup  O(1) avg – direct key access
"""


# ------------------------------------------------------------------
# 1. Linear Search — O(n)
# Check each element until we find a match or exhaust the list.
# Works on ANY list (sorted or unsorted).
# ------------------------------------------------------------------
def linear_search(cases, query, field="case_id"):
    """
    Search through `cases` (list of dicts) for one matching `query` on `field`.
    Returns a list of matching case dicts (could be many if field is not unique).
    """
    results = []
    for case in cases:             # O(n) — we may look at every case
        if query.lower() in str(case.get(field, "")).lower():
            results.append(case)
    return results


# ------------------------------------------------------------------
# 2. Binary Search — O(log n)
# The list MUST be sorted by Case ID before calling this.
# We keep halving the search range until the target is found.
# ------------------------------------------------------------------
def binary_search(sorted_cases, target_id):
    """
    Search `sorted_cases` (sorted by 'case_id') for `target_id`.
    Returns the matching case dict or None.
    """
    low = 0
    high = len(sorted_cases) - 1

    while low <= high:
        mid = (low + high) // 2                # find the middle index
        mid_id = sorted_cases[mid].get("case_id", "")

        if mid_id == target_id:
            return sorted_cases[mid]           # exact match found
        elif mid_id < target_id:
            low = mid + 1                      # target is in the RIGHT half
        else:
            high = mid - 1                     # target is in the LEFT half

    return None  # not found


# ------------------------------------------------------------------
# 3. Dictionary / Hash Lookup — O(1) average
# Python dict uses a hash table internally.
# Given a Case ID string we get the case directly without scanning.
# ------------------------------------------------------------------
def hash_lookup(case_dict, target_id):
    """
    Perform an O(1) average dictionary lookup.
    `case_dict` maps case_id -> case dict.
    Returns the matching case or None.
    """
    return case_dict.get(target_id)   # hash table lookup
