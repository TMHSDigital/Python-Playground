"""Built-in collections: lists, tuples, sets, dicts, and their operations.

Python's built-in collection types cover most use cases. This module
demonstrates idiomatic usage patterns and lesser-known features.
"""

from __future__ import annotations

from collections import Counter, OrderedDict, defaultdict, deque, namedtuple


# --- Lists ---


def rotate_list(items: list, k: int) -> list:
    """Rotate a list to the right by k positions."""
    if not items:
        return items
    k = k % len(items)
    return items[-k:] + items[:-k]


def interleave(*lists: list) -> list:
    """Interleave multiple lists: [a1,b1,a2,b2,...].

    Stops at the shortest list.
    """
    return [item for group in zip(*lists) for item in group]


def deduplicate_preserve_order(items: list) -> list:
    """Remove duplicates while preserving insertion order."""
    seen: set = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# --- Tuples and Named Tuples ---

Point = namedtuple("Point", ["x", "y"])


def distance(p1: Point, p2: Point) -> float:
    """Euclidean distance between two points."""
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


# --- Dictionaries ---


def merge_dicts(*dicts: dict) -> dict:
    """Merge multiple dicts (later values override earlier)."""
    result: dict = {}
    for d in dicts:
        result |= d
    return result


def deep_get(d: dict, keys: list[str], default=None):
    """Safely traverse nested dicts with a list of keys."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d


# --- defaultdict ---


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other."""
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word.lower()))
        groups[key].append(word)
    return list(groups.values())


# --- Counter ---


def most_common_words(text: str, n: int = 5) -> list[tuple[str, int]]:
    """Find the n most common words in text."""
    words = text.lower().split()
    return Counter(words).most_common(n)


def are_anagrams(a: str, b: str) -> bool:
    """Check if two strings are anagrams using Counter."""
    return Counter(a.lower().replace(" ", "")) == Counter(b.lower().replace(" ", ""))


# --- Deque ---


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """Find the maximum in each sliding window of size k.

    Uses deque for O(n) performance.
    """
    if not nums or k <= 0:
        return []

    result: list[int] = []
    dq: deque[int] = deque()  # stores indices

    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def recent_items(capacity: int) -> deque:
    """Create a bounded deque that automatically drops old items."""
    return deque(maxlen=capacity)


# --- Sets ---


def jaccard_similarity(a: set, b: set) -> float:
    """Compute Jaccard similarity between two sets."""
    if not a and not b:
        return 1.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union


def symmetric_diff_items(a: set, b: set) -> set:
    """Items in either set but not both."""
    return a ^ b


if __name__ == "__main__":
    print("=== rotate_list ===")
    print(f"  {rotate_list([1, 2, 3, 4, 5], 2)}")

    print("\n=== interleave ===")
    print(f"  {interleave([1, 2, 3], ['a', 'b', 'c'])}")

    print("\n=== deduplicate_preserve_order ===")
    print(f"  {deduplicate_preserve_order([3, 1, 4, 1, 5, 9, 2, 6, 5])}")

    print("\n=== namedtuple distance ===")
    p1, p2 = Point(0, 0), Point(3, 4)
    print(f"  {p1} -> {p2}: {distance(p1, p2)}")

    print("\n=== deep_get ===")
    data = {"user": {"profile": {"name": "Alice"}}}
    print(f"  {deep_get(data, ['user', 'profile', 'name'])}")
    print(f"  {deep_get(data, ['user', 'missing'], 'N/A')}")

    print("\n=== group_anagrams ===")
    print(f"  {group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])}")

    print("\n=== most_common_words ===")
    text = "the cat sat on the mat the cat"
    print(f"  {most_common_words(text, 3)}")

    print("\n=== sliding_window_max ===")
    print(f"  {sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)}")

    print("\n=== jaccard_similarity ===")
    print(f"  {jaccard_similarity({1, 2, 3}, {2, 3, 4}):.2f}")
