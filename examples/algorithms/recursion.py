"""Recursion: classic problems and techniques.

Recursion solves problems by breaking them into smaller subproblems.
This module covers essential recursive patterns including divide-and-conquer,
backtracking, and dynamic programming with memoization.
"""

from __future__ import annotations

import functools


# --- Classic Recursion ---


def factorial(n: int) -> int:
    """Compute n! recursively. O(n) time and space."""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number with memoization. O(n) time."""

    @functools.lru_cache(maxsize=None)
    def fib(k: int) -> int:
        if k < 2:
            return k
        return fib(k - 1) + fib(k - 2)

    return fib(n)


def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclid's algorithm."""
    if b == 0:
        return abs(a)
    return gcd(b, a % b)


def power(base: float, exp: int) -> float:
    """Fast exponentiation using repeated squaring. O(log n) time."""
    if exp == 0:
        return 1
    if exp < 0:
        return 1 / power(base, -exp)
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)


# --- Divide and Conquer ---


def max_subarray_sum(arr: list[int]) -> int:
    """Find the maximum contiguous subarray sum (Kadane's algorithm variant).

    Uses divide-and-conquer approach: O(n log n) time.
    """
    if not arr:
        return 0

    def _max_crossing_sum(arr: list[int], low: int, mid: int, high: int) -> int:
        left_sum = float("-inf")
        total = 0
        for i in range(mid, low - 1, -1):
            total += arr[i]
            left_sum = max(left_sum, total)

        right_sum = float("-inf")
        total = 0
        for i in range(mid + 1, high + 1):
            total += arr[i]
            right_sum = max(right_sum, total)

        return int(left_sum + right_sum)

    def _max_subarray(arr: list[int], low: int, high: int) -> int:
        if low == high:
            return arr[low]
        mid = (low + high) // 2
        return max(
            _max_subarray(arr, low, mid),
            _max_subarray(arr, mid + 1, high),
            _max_crossing_sum(arr, low, mid, high),
        )

    return _max_subarray(arr, 0, len(arr) - 1)


# --- Backtracking ---


def permutations(items: list) -> list[list]:
    """Generate all permutations of a list."""
    if len(items) <= 1:
        return [items[:]]

    result: list[list] = []
    for i in range(len(items)):
        rest = items[:i] + items[i + 1 :]
        for perm in permutations(rest):
            result.append([items[i]] + perm)
    return result


def n_queens(n: int) -> list[list[int]]:
    """Solve the N-Queens problem using backtracking.

    Returns all solutions as lists of column positions for each row.
    """
    solutions: list[list[int]] = []

    def _is_safe(queens: list[int], row: int, col: int) -> bool:
        for r, c in enumerate(queens):
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def _solve(queens: list[int]) -> None:
        row = len(queens)
        if row == n:
            solutions.append(queens[:])
            return
        for col in range(n):
            if _is_safe(queens, row, col):
                queens.append(col)
                _solve(queens)
                queens.pop()

    _solve([])
    return solutions


def subsets(items: list) -> list[list]:
    """Generate all subsets (power set) of a list."""
    if not items:
        return [[]]
    rest = subsets(items[1:])
    return rest + [[items[0]] + s for s in rest]


# --- Dynamic Programming (recursive with memoization) ---


def coin_change(coins: list[int], amount: int) -> int:
    """Find the minimum number of coins needed to make the given amount.

    Returns -1 if it's not possible.
    """

    @functools.lru_cache(maxsize=None)
    def dp(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float("inf")
        return min((dp(remaining - c) + 1 for c in coins), default=float("inf"))

    result = dp(amount)
    return result if result != float("inf") else -1


def longest_common_subsequence(s1: str, s2: str) -> str:
    """Find the longest common subsequence of two strings."""

    @functools.lru_cache(maxsize=None)
    def dp(i: int, j: int) -> str:
        if i == len(s1) or j == len(s2):
            return ""
        if s1[i] == s2[j]:
            return s1[i] + dp(i + 1, j + 1)
        opt1 = dp(i + 1, j)
        opt2 = dp(i, j + 1)
        return opt1 if len(opt1) >= len(opt2) else opt2

    return dp(0, 0)


# --- Tower of Hanoi ---


def tower_of_hanoi(
    n: int, source: str = "A", target: str = "C", auxiliary: str = "B"
) -> list[tuple[str, str]]:
    """Solve Tower of Hanoi, returning the sequence of moves."""
    moves: list[tuple[str, str]] = []

    def _solve(disks: int, src: str, tgt: str, aux: str) -> None:
        if disks == 1:
            moves.append((src, tgt))
            return
        _solve(disks - 1, src, aux, tgt)
        moves.append((src, tgt))
        _solve(disks - 1, aux, tgt, src)

    _solve(n, source, target, auxiliary)
    return moves


if __name__ == "__main__":
    print("=== Factorial ===")
    for n in [0, 1, 5, 10]:
        print(f"  {n}! = {factorial(n)}")

    print("\n=== Fibonacci ===")
    fibs = [fibonacci(i) for i in range(12)]
    print(f"  {fibs}")

    print("\n=== GCD ===")
    print(f"  gcd(48, 18) = {gcd(48, 18)}")

    print("\n=== Power ===")
    print(f"  2^10 = {power(2, 10)}")
    print(f"  3^-2 = {power(3, -2):.6f}")

    print("\n=== Max Subarray Sum ===")
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"  {arr} -> {max_subarray_sum(arr)}")

    print("\n=== Permutations ===")
    print(f"  [1,2,3] -> {permutations([1, 2, 3])}")

    print("\n=== N-Queens (4x4) ===")
    solutions = n_queens(4)
    print(f"  {len(solutions)} solutions: {solutions}")

    print("\n=== Coin Change ===")
    print(f"  coins=[1,5,10,25], amount=67 -> {coin_change([1, 5, 10, 25], 67)} coins")

    print("\n=== LCS ===")
    print(
        f"  'ABCBDAB' & 'BDCAB' -> '{longest_common_subsequence('ABCBDAB', 'BDCAB')}'"
    )

    print("\n=== Tower of Hanoi (3 disks) ===")
    moves = tower_of_hanoi(3)
    for src, tgt in moves:
        print(f"  {src} -> {tgt}")
