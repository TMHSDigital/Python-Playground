"""Sorting algorithms: implementations and comparisons.

Each algorithm includes its time and space complexity. These are educational
implementations -- in production, use Python's built-in sorted() / list.sort()
which use Timsort (O(n log n) hybrid of merge sort and insertion sort).
"""

from __future__ import annotations


def bubble_sort(arr: list) -> list:
    """Bubble Sort -- O(n^2) time, O(1) space.

    Repeatedly swaps adjacent elements if they're in the wrong order.
    Simple but inefficient for large datasets.
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr: list) -> list:
    """Insertion Sort -- O(n^2) time, O(1) space.

    Builds the sorted array one element at a time. Efficient for
    small or nearly-sorted datasets.
    """
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def selection_sort(arr: list) -> list:
    """Selection Sort -- O(n^2) time, O(1) space.

    Finds the minimum element and puts it at the beginning, then
    repeats for the remaining unsorted portion.
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr: list) -> list:
    """Merge Sort -- O(n log n) time, O(n) space.

    Divides the array in half, recursively sorts each half,
    then merges them back together.
    """
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(arr: list) -> list:
    """Quick Sort -- O(n log n) average, O(n^2) worst, O(log n) space.

    Picks a pivot, partitions around it, then recursively sorts
    the partitions. Uses median-of-three pivot selection.
    """
    if len(arr) <= 1:
        return arr.copy()

    arr = arr.copy()
    _quicksort(arr, 0, len(arr) - 1)
    return arr


def _quicksort(arr: list, low: int, high: int) -> None:
    if low < high:
        pivot = _partition(arr, low, high)
        _quicksort(arr, low, pivot - 1)
        _quicksort(arr, pivot + 1, high)


def _partition(arr: list, low: int, high: int) -> int:
    # Median-of-three pivot
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    arr[mid], arr[high] = arr[high], arr[mid]

    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def counting_sort(arr: list[int]) -> list[int]:
    """Counting Sort -- O(n + k) time and space where k = max value.

    Non-comparison sort that works well when the range of values is small.
    Only works for non-negative integers.
    """
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([i] * c)
    return result


def is_sorted(arr: list) -> bool:
    """Check if a list is sorted in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


if __name__ == "__main__":
    import random
    import time

    test_data = random.sample(range(1000), 200)

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Insertion Sort", insertion_sort),
        ("Selection Sort", selection_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quicksort),
    ]

    print(f"Sorting {len(test_data)} random elements:\n")
    for name, func in algorithms:
        start = time.perf_counter()
        result = func(test_data)
        elapsed = time.perf_counter() - start
        assert is_sorted(result), f"{name} failed!"
        print(f"  {name:20s} {elapsed*1000:8.2f} ms")

    print(f"\n  {'Python sorted()':20s}", end="")
    start = time.perf_counter()
    sorted(test_data)
    elapsed = time.perf_counter() - start
    print(f" {elapsed*1000:8.2f} ms")
