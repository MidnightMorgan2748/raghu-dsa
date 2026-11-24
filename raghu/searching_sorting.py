"""Searching and sorting algorithms.

Every sort returns a new list and leaves the input untouched. Each accepts an
optional ``key`` function with the same meaning as in :func:`sorted`.
"""

import random
from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")
KeyFunc = Optional[Callable[[Any], Any]]

__all__ = [
    "binary_search",
    "bubble_sort",
    "heap_sort",
    "insertion_sort",
    "linear_search",
    "merge_sort",
    "quick_sort",
    "selection_sort",
]


def _identity(x: Any) -> Any:
    return x


def linear_search(arr: Sequence[T], target: T) -> int:
    """Return the index of the first occurrence of ``target``, or -1.

    Time: O(n). Space: O(1).
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr: Sequence[T], target: T, *, recursive: bool = False) -> int:
    """Return an index of ``target`` in sorted ``arr``, or -1 if absent.

    ``arr`` must be sorted in ascending order. If ``target`` occurs several
    times, any matching index may be returned.

    Args:
        arr: Sorted sequence.
        target: Value to find.
        recursive: Use the recursive implementation instead of the iterative one.

    Time: O(log n). Space: O(1) iterative, O(log n) recursive.
    """
    if recursive:
        return _binary_search_recursive(arr, target, 0, len(arr) - 1)
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        value = arr[mid]
        if value == target:
            return mid
        if value < target:  # type: ignore[operator]
            low = mid + 1
        else:
            high = mid - 1
    return -1


def _binary_search_recursive(arr: Sequence[T], target: T, low: int, high: int) -> int:
    if low > high:
        return -1
    mid = low + (high - low) // 2
    value = arr[mid]
    if value == target:
        return mid
    if value < target:  # type: ignore[operator]
        return _binary_search_recursive(arr, target, mid + 1, high)
    return _binary_search_recursive(arr, target, low, mid - 1)


def bubble_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using bubble sort with early exit. Stable.

    Time: O(n^2) worst/average, O(n) best (already sorted). Space: O(n) for the copy.
    """
    data = list(arr)
    k = key or _identity
    n = len(data)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if k(data[i + 1]) < k(data[i]):
                data[i], data[i + 1] = data[i + 1], data[i]
                swapped = True
        if not swapped:
            break
    return data


def selection_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using selection sort. Not stable.

    Time: O(n^2) in all cases. Space: O(n) for the copy.
    """
    data = list(arr)
    k = key or _identity
    n = len(data)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if k(data[j]) < k(data[smallest]):
                smallest = j
        if smallest != i:
            data[i], data[smallest] = data[smallest], data[i]
    return data


def insertion_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using insertion sort. Stable.

    Time: O(n^2) worst/average, O(n) best. Space: O(n) for the copy.
    """
    data = list(arr)
    k = key or _identity
    for i in range(1, len(data)):
        current = data[i]
        current_key = k(current)
        j = i - 1
        while j >= 0 and k(data[j]) > current_key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = current
    return data


def merge_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using top-down merge sort. Stable.

    Time: O(n log n) in all cases. Space: O(n).
    """
    k = key or _identity
    return _merge_sort(list(arr), k)


def _merge_sort(data: List[T], k: Callable[[Any], Any]) -> List[T]:
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = _merge_sort(data[:mid], k)
    right = _merge_sort(data[mid:], k)
    merged: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if k(right[j]) < k(left[i]):
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using in-place quick sort with a random pivot and 3-way partitioning. Not stable.

    Three-way partitioning keeps inputs with many duplicates fast, and recursing
    into the smaller partition first bounds stack depth to O(log n).

    Time: O(n log n) expected, O(n^2) worst case. Space: O(n) for the copy plus O(log n) stack.
    """
    data = list(arr)
    k = key or _identity

    def sort(lo: int, hi: int) -> None:
        while lo < hi:
            pivot = k(data[random.randint(lo, hi)])
            lt, i, gt = lo, lo, hi
            while i <= gt:
                current = k(data[i])
                if current < pivot:
                    data[lt], data[i] = data[i], data[lt]
                    lt += 1
                    i += 1
                elif pivot < current:
                    data[i], data[gt] = data[gt], data[i]
                    gt -= 1
                else:
                    i += 1
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(data) - 1)
    return data


def heap_sort(arr: Sequence[T], key: KeyFunc = None) -> List[T]:
    """Sort using heap sort with an in-place binary max-heap. Not stable.

    Time: O(n log n) in all cases. Space: O(n) for the copy, O(1) extra.
    """
    data = list(arr)
    k = key or _identity
    n = len(data)

    def sift_down(root: int, size: int) -> None:
        while True:
            child = 2 * root + 1
            if child >= size:
                return
            if child + 1 < size and k(data[child]) < k(data[child + 1]):
                child += 1
            if k(data[root]) < k(data[child]):
                data[root], data[child] = data[child], data[root]
                root = child
            else:
                return

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n)
    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sift_down(0, end)
    return data
