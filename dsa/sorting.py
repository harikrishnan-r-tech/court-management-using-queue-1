"""
Sorting Algorithms
===================
Bubble Sort implemented manually.
Time Complexity: O(n^2) in average/worst case, O(n) best case (already sorted).

Bubble Sort works by repeatedly swapping adjacent elements that are
out of order. Each full pass 'bubbles' the largest unsorted element
to its correct position at the end.
"""


def bubble_sort(cases, key_func, reverse=False):
    """
    Sort a list of case dicts in-place using Bubble Sort.

    Args:
        cases    : list of case dicts
        key_func : a function that extracts the comparison key from a case
        reverse  : if True, sort in descending order

    Returns the sorted list (same reference, mutated in-place).
    """
    n = len(cases)

    for i in range(n):                           # O(n) outer passes
        swapped = False

        for j in range(0, n - i - 1):            # O(n) inner comparisons
            a = key_func(cases[j])
            b = key_func(cases[j + 1])

            # Decide whether to swap based on sort direction
            should_swap = (a > b) if not reverse else (a < b)

            if should_swap:
                # Swap adjacent elements
                cases[j], cases[j + 1] = cases[j + 1], cases[j]
                swapped = True

        # Early exit optimisation: if no swap happened in this pass,
        # the list is already sorted — best case O(n)
        if not swapped:
            break

    return cases


# ----- Key functions for each sort criterion -----

def key_case_id(case):
    """Sort key: Case ID string (lexicographic — works for C001-C999)."""
    return case.get("case_id", "")


_PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def key_priority(case):
    """Sort key: Priority integer (High=0, Medium=1, Low=2)."""
    return _PRIORITY_ORDER.get(case.get("priority", "Low"), 2)


def key_filing_date(case):
    """Sort key: Filing date string (ISO format sorts correctly as string)."""
    return case.get("filing_date", "9999-12-31")
