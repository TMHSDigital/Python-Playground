"""Comprehensions: list, dict, set, and generator expressions.

Comprehensions are a concise, readable way to create collections from
iterables. This module shows the patterns and when to use each type.
"""

from __future__ import annotations

import math
from collections.abc import Iterator


# --- List Comprehensions ---


def squares(n: int) -> list[int]:
    """Return squares of 0..n-1."""
    return [x**2 for x in range(n)]


def evens_only(numbers: list[int]) -> list[int]:
    """Filter to keep only even numbers."""
    return [x for x in numbers if x % 2 == 0]


def flatten_2d(matrix: list[list]) -> list:
    """Flatten a 2D list into 1D using a nested comprehension."""
    return [item for row in matrix for item in row]


def transpose(matrix: list[list]) -> list[list]:
    """Transpose a 2D matrix."""
    if not matrix:
        return []
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


# --- Dict Comprehensions ---


def invert_dict(d: dict) -> dict:
    """Swap keys and values (assumes unique values)."""
    return {v: k for k, v in d.items()}


def index_by(items: list[dict], key: str) -> dict:
    """Index a list of dicts by a specific key field."""
    return {item[key]: item for item in items if key in item}


def word_lengths(words: list[str]) -> dict[str, int]:
    """Map each word to its length."""
    return {word: len(word) for word in words}


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Group words by their length.

    Note: this uses a loop because grouping can't be done in a single
    dict comprehension without overwriting.
    """
    groups: dict[int, list[str]] = {}
    for word in words:
        groups.setdefault(len(word), []).append(word)
    return groups


# --- Set Comprehensions ---


def unique_chars(text: str) -> set[str]:
    """Get unique alphabetic characters from text (lowercased)."""
    return {ch.lower() for ch in text if ch.isalpha()}


def common_elements(a: list, b: list) -> set:
    """Find common elements between two lists using sets."""
    return {x for x in a if x in set(b)}


# --- Generator Expressions ---


def sum_of_squares(n: int) -> int:
    """Sum of squares using a generator expression (memory-efficient)."""
    return sum(x**2 for x in range(n))


def first_matching(items: list, predicate) -> object | None:
    """Find the first item matching a predicate using next()."""
    return next((x for x in items if predicate(x)), None)


def fibonacci_gen(limit: int) -> Iterator[int]:
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


# --- Practical Examples ---


def prime_sieve(n: int) -> list[int]:
    """Sieve of Eratosthenes using comprehensions."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def pascal_triangle(rows: int) -> list[list[int]]:
    """Generate Pascal's triangle using comprehensions."""
    triangle: list[list[int]] = []
    for r in range(rows):
        if r == 0:
            triangle.append([1])
        else:
            prev = triangle[r - 1]
            row = [1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1]
            triangle.append(row)
    return triangle


def matrix_multiply(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Multiply two matrices using nested comprehensions."""
    rows_a, cols_b = len(a), len(b[0])
    cols_a = len(a[0])
    return [
        [sum(a[i][k] * b[k][j] for k in range(cols_a)) for j in range(cols_b)]
        for i in range(rows_a)
    ]


if __name__ == "__main__":
    print("=== Squares ===")
    print(f"  {squares(10)}")

    print("\n=== Flatten 2D ===")
    print(f"  {flatten_2d([[1, 2], [3, 4], [5, 6]])}")

    print("\n=== Transpose ===")
    m = [[1, 2, 3], [4, 5, 6]]
    print(f"  {m} -> {transpose(m)}")

    print("\n=== Invert Dict ===")
    print(f"  {invert_dict({'a': 1, 'b': 2, 'c': 3})}")

    print("\n=== Group by Length ===")
    words = ["cat", "dog", "fish", "bird", "ant", "bear"]
    print(f"  {group_by_length(words)}")

    print("\n=== Primes up to 50 ===")
    print(f"  {prime_sieve(50)}")

    print("\n=== Pascal's Triangle (5 rows) ===")
    for row in pascal_triangle(5):
        print(f"  {row}")

    print("\n=== Fibonacci up to 100 ===")
    print(f"  {list(fibonacci_gen(100))}")
