"""Functions: definitions, arguments, closures, and higher-order functions.

Covers default args, *args/**kwargs, lambda, closures, and functools utilities.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


# --- Basic Functions ---


def greet(name: str, greeting: str = "Hello") -> str:
    """Greet someone with an optional greeting word."""
    return f"{greeting}, {name}!"


def multi_return(x: int) -> tuple[int, int, int]:
    """Return multiple values as a tuple (a common Python idiom)."""
    return x, x**2, x**3


# --- *args and **kwargs ---


def flexible_sum(*args: int | float) -> int | float:
    """Sum any number of numeric arguments."""
    return sum(args)


def build_url(base: str, **params: str) -> str:
    """Build a URL with query parameters from keyword arguments."""
    if not params:
        return base
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{query}"


# --- First-Class Functions ---


def apply_twice(func: Callable[[T], T], value: T) -> T:
    """Apply a function twice to a value: f(f(x))."""
    return func(func(value))


def compose(f: Callable, g: Callable) -> Callable:
    """Compose two functions: compose(f, g)(x) == f(g(x))."""
    return lambda x: f(g(x))


# --- Lambda ---


def sort_by_last_char(words: list[str]) -> list[str]:
    """Sort a list of words by their last character."""
    return sorted(words, key=lambda w: w[-1])


# --- Closures ---


def make_counter(start: int = 0) -> Callable[[], int]:
    """Create a counter function that increments on each call.

    Demonstrates closures and the `nonlocal` keyword.
    """
    count = start

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def make_multiplier(factor: int | float) -> Callable[[int | float], int | float]:
    """Return a function that multiplies its input by factor."""
    return lambda x: x * factor


# --- functools ---


def memoized_fibonacci(n: int) -> int:
    """Compute Fibonacci using functools.lru_cache for memoization."""

    @functools.lru_cache(maxsize=None)
    def fib(k: int) -> int:
        if k < 2:
            return k
        return fib(k - 1) + fib(k - 2)

    return fib(n)


def pipeline(*functions: Callable) -> Callable:
    """Chain multiple functions into a single pipeline using reduce.

    pipeline(f, g, h)(x) == h(g(f(x)))
    """
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


# --- Partial Application ---


def power(base: int | float, exponent: int | float) -> int | float:
    """Raise base to exponent."""
    return base**exponent


square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)


# --- Recursion ---


def flatten(nested: list) -> list:
    """Recursively flatten arbitrarily nested lists."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    print("=== greet ===")
    print(f"  {greet('Alice')}")
    print(f"  {greet('Bob', 'Howdy')}")

    print("\n=== multi_return ===")
    val, sq, cb = multi_return(3)
    print(f"  3 -> value={val}, square={sq}, cube={cb}")

    print("\n=== flexible_sum ===")
    print(f"  sum(1,2,3,4,5) = {flexible_sum(1, 2, 3, 4, 5)}")

    print("\n=== build_url ===")
    print(f"  {build_url('https://api.example.com/search', q='python', page='1')}")

    print("\n=== apply_twice ===")
    print(f"  double(double(3)) = {apply_twice(lambda x: x * 2, 3)}")

    print("\n=== make_counter ===")
    counter = make_counter()
    print(f"  calls: {counter()}, {counter()}, {counter()}")

    print("\n=== pipeline ===")
    transform = pipeline(str.strip, str.lower, str.title)
    print(f"  '  hello world  ' -> {transform('  hello world  ')!r}")

    print("\n=== square / cube ===")
    print(f"  square(5) = {square(5)}, cube(3) = {cube(3)}")

    print("\n=== flatten ===")
    print(f"  {flatten([1, [2, [3, 4], 5], [6]])}")

    print("\n=== memoized_fibonacci ===")
    print(f"  fib(30) = {memoized_fibonacci(30)}")
