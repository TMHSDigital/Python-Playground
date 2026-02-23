"""Decorators: function and class decorators with practical examples.

Decorators are a way to modify or extend functions/classes without changing
their source code. They're one of Python's most powerful features.
"""

from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


# --- Basic Function Decorators ---


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure and print execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.6f}s")
        return result

    return wrapper


def debug(func: Callable[P, R]) -> Callable[P, R]:
    """Print function signature and return value on each call."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  -> {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  <- {func.__name__} = {result!r}")
        return result

    return wrapper


# --- Decorators with Arguments ---


def repeat(n: int) -> Callable:
    """Call the decorated function n times and return last result."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result  # type: ignore[return-value]

        return wrapper

    return decorator


def validate_types(**type_hints: type) -> Callable:
    """Validate argument types at runtime.

    Usage: @validate_types(x=int, y=str)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import inspect

            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, expected_type in type_hints.items():
                if name in bound.arguments:
                    value = bound.arguments[name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_with_ttl(ttl_seconds: float) -> Callable:
    """Cache function results with a time-to-live expiration."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict[tuple, tuple[float, R]] = {}

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            if key in cache:
                cached_time, cached_result = cache[key]
                if now - cached_time < ttl_seconds:
                    return cached_result

            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        wrapper.clear_cache = cache.clear  # type: ignore[attr-defined]
        return wrapper

    return decorator


# --- Decorator Stacking ---


def bold(func: Callable[..., str]) -> Callable[..., str]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return f"<b>{func(*args, **kwargs)}</b>"

    return wrapper


def italic(func: Callable[..., str]) -> Callable[..., str]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        return f"<i>{func(*args, **kwargs)}</i>"

    return wrapper


# --- Class Decorators ---


def singleton(cls: type) -> type:
    """Make a class a singleton using a decorator."""
    instances: dict[type, Any] = {}

    @functools.wraps(cls, updated=[])
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance  # type: ignore[return-value]


def auto_repr(cls: type) -> type:
    """Automatically generate __repr__ from __init__ parameters."""
    import inspect

    sig = inspect.signature(cls.__init__)
    params = [p for p in sig.parameters if p != "self"]

    def __repr__(self: Any) -> str:
        values = ", ".join(f"{p}={getattr(self, p)!r}" for p in params)
        return f"{cls.__name__}({values})"

    cls.__repr__ = __repr__
    return cls


# --- Method Decorators ---


def deprecated(message: str = "") -> Callable:
    """Mark a function as deprecated with an optional message."""
    import warnings

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            msg = f"{func.__name__} is deprecated."
            if message:
                msg += f" {message}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":
    print("=== @timer ===")

    @timer
    def slow_add(a: int, b: int) -> int:
        time.sleep(0.01)
        return a + b

    slow_add(1, 2)

    print("\n=== @debug ===")

    @debug
    def multiply(x: int, y: int) -> int:
        return x * y

    multiply(3, 4)

    print("\n=== @repeat(3) ===")

    @repeat(3)
    def say_hello(name: str) -> str:
        print(f"  Hello, {name}!")
        return f"greeted {name}"

    say_hello("World")

    print("\n=== @validate_types ===")

    @validate_types(x=int, y=int)
    def safe_add(x: int, y: int) -> int:
        return x + y

    print(f"  safe_add(3, 4) = {safe_add(3, 4)}")
    try:
        safe_add("3", 4)  # type: ignore[arg-type]
    except TypeError as e:
        print(f"  Error: {e}")

    print("\n=== Stacking: @bold @italic ===")

    @bold
    @italic
    def greet(name: str) -> str:
        return f"Hello, {name}"

    print(f"  {greet('Alice')}")

    print("\n=== @auto_repr ===")

    @auto_repr
    class Point:
        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y

    print(f"  {Point(1.0, 2.0)!r}")
