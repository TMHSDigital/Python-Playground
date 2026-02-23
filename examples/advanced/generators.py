"""Generators and iterators: lazy evaluation and memory-efficient processing.

Generators produce values on demand instead of computing everything upfront.
They're ideal for large datasets, infinite sequences, and pipeline processing.
"""

from __future__ import annotations

import itertools
from collections.abc import Generator, Iterator
from typing import TypeVar

T = TypeVar("T")


# --- Basic Generators ---


def count_up(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """Infinite counter starting from `start`."""
    n = start
    while True:
        yield n
        n += step


def take(n: int, iterable) -> list:
    """Take the first n items from any iterable."""
    return list(itertools.islice(iterable, n))


def range_float(start: float, stop: float, step: float) -> Generator[float, None, None]:
    """Like range() but for floats."""
    current = start
    while current < stop:
        yield round(current, 10)
        current += step


# --- Generator Pipelines ---


def read_lines(text: str) -> Generator[str, None, None]:
    """Simulate reading lines from a file."""
    for line in text.split("\n"):
        yield line


def strip_lines(lines: Iterator[str]) -> Generator[str, None, None]:
    for line in lines:
        yield line.strip()


def non_empty(lines: Iterator[str]) -> Generator[str, None, None]:
    for line in lines:
        if line:
            yield line


def to_upper(lines: Iterator[str]) -> Generator[str, None, None]:
    for line in lines:
        yield line.upper()


def process_text(text: str) -> list[str]:
    """Chain generators into a processing pipeline.

    Each stage processes one item at a time, keeping memory usage constant
    regardless of input size.
    """
    pipeline = to_upper(non_empty(strip_lines(read_lines(text))))
    return list(pipeline)


# --- Generator Expressions vs List Comprehensions ---


def sum_squares_gen(n: int) -> int:
    """Sum of squares using a generator expression.

    Unlike [x**2 for x in range(n)], this doesn't create an intermediate list.
    """
    return sum(x**2 for x in range(n))


def any_negative(numbers: list[int | float]) -> bool:
    """Check if any number is negative (short-circuits)."""
    return any(x < 0 for x in numbers)


# --- yield from ---


def flatten_nested(items) -> Generator:
    """Recursively flatten nested iterables using `yield from`."""
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten_nested(item)
        else:
            yield item


def chain_iterables(*iterables) -> Generator:
    """Combine multiple iterables (like itertools.chain)."""
    for iterable in iterables:
        yield from iterable


# --- Coroutine-style Generators (send/throw) ---


def running_average() -> Generator[float, float, None]:
    """A coroutine that computes a running average.

    Send values with .send(value), receive the current average.
    """
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


# --- Practical: Sliding Window ---


def sliding_window(iterable, size: int) -> Generator[tuple, None, None]:
    """Yield overlapping windows of `size` from an iterable."""
    it = iter(iterable)
    window = tuple(itertools.islice(it, size))
    if len(window) == size:
        yield window
    for item in it:
        window = window[1:] + (item,)
        yield window


# --- Practical: Batch Processing ---


def batched(iterable, n: int) -> Generator[tuple, None, None]:
    """Split an iterable into batches of size n.

    Similar to itertools.batched (Python 3.12+).
    """
    it = iter(iterable)
    while True:
        batch = tuple(itertools.islice(it, n))
        if not batch:
            break
        yield batch


# --- Practical: File-like Processing ---


def grep(pattern: str, lines: Iterator[str]) -> Generator[str, None, None]:
    """Filter lines containing the pattern (like Unix grep)."""
    for line in lines:
        if pattern in line:
            yield line


def head(n: int, lines: Iterator[str]) -> Generator[str, None, None]:
    """Take the first n lines (like Unix head)."""
    for i, line in enumerate(lines):
        if i >= n:
            break
        yield line


if __name__ == "__main__":
    print("=== Infinite Counter (first 10) ===")
    print(f"  {take(10, count_up())}")

    print("\n=== Float Range ===")
    print(f"  {list(range_float(0, 1, 0.2))}")

    print("\n=== Text Pipeline ===")
    sample = "  hello  \n  \n  world  \n  python  \n  "
    print(f"  {process_text(sample)}")

    print("\n=== Flatten ===")
    nested = [1, [2, [3, 4]], [5, (6, 7)], 8]
    print(f"  {list(flatten_nested(nested))}")

    print("\n=== Running Average ===")
    avg = running_average()
    next(avg)
    for val in [10, 20, 30, 40]:
        result = avg.send(val)
        print(f"  sent {val}, average = {result}")

    print("\n=== Sliding Window ===")
    print(f"  {list(sliding_window(range(6), 3))}")

    print("\n=== Batched ===")
    print(f"  {list(batched(range(10), 3))}")
