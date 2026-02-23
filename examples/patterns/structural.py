"""Structural design patterns: Decorator, Adapter, and Proxy.

Structural patterns deal with object composition, creating relationships
between objects to form larger structures.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any


# --- Decorator Pattern (class-based) ---


class TextProcessor(ABC):
    """Abstract text processing interface."""

    @abstractmethod
    def process(self, text: str) -> str: ...


class PlainText(TextProcessor):
    def process(self, text: str) -> str:
        return text


class UpperCaseDecorator(TextProcessor):
    def __init__(self, wrapped: TextProcessor) -> None:
        self._wrapped = wrapped

    def process(self, text: str) -> str:
        return self._wrapped.process(text).upper()


class TrimDecorator(TextProcessor):
    def __init__(self, wrapped: TextProcessor) -> None:
        self._wrapped = wrapped

    def process(self, text: str) -> str:
        return self._wrapped.process(text).strip()


class BorderDecorator(TextProcessor):
    def __init__(self, wrapped: TextProcessor, char: str = "*") -> None:
        self._wrapped = wrapped
        self._char = char

    def process(self, text: str) -> str:
        result = self._wrapped.process(text)
        border = self._char * (len(result) + 4)
        return f"{border}\n{self._char} {result} {self._char}\n{border}"


# --- Decorator Pattern (Pythonic function decorators) ---


def retry(max_attempts: int = 3, delay: float = 0.1) -> Callable:
    """Retry a function on exception up to max_attempts times."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception  # type: ignore[misc]

        return wrapper

    return decorator


def log_calls(func: Callable) -> Callable:
    """Log function calls with arguments and return values."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result

    return wrapper


# --- Adapter Pattern ---


class LegacyPrinter:
    """An old-style printer with a non-standard interface."""

    def print_document(self, doc_text: str) -> str:
        return f"[LEGACY] Printing: {doc_text}"


class ModernPrinter(ABC):
    """Modern printer interface."""

    @abstractmethod
    def print(self, content: str, copies: int = 1) -> str: ...


class PrinterAdapter(ModernPrinter):
    """Adapts LegacyPrinter to the ModernPrinter interface."""

    def __init__(self, legacy: LegacyPrinter) -> None:
        self._legacy = legacy

    def print(self, content: str, copies: int = 1) -> str:
        results = []
        for _ in range(copies):
            results.append(self._legacy.print_document(content))
        return "\n".join(results)


# --- Proxy Pattern ---


@dataclass
class HeavyResource:
    """Simulates an expensive-to-create resource."""

    name: str
    _data: str = field(init=False, default="")

    def __post_init__(self) -> None:
        self._data = f"Heavy data for {self.name}"

    def get_data(self) -> str:
        return self._data


class LazyProxy:
    """Lazy-loading proxy that defers creation of HeavyResource.

    The real object is only created when first accessed.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._resource: HeavyResource | None = None

    def _ensure_loaded(self) -> HeavyResource:
        if self._resource is None:
            self._resource = HeavyResource(self._name)
        return self._resource

    def get_data(self) -> str:
        return self._ensure_loaded().get_data()

    @property
    def is_loaded(self) -> bool:
        return self._resource is not None


class CachingProxy:
    """Proxy that caches the results of an expensive function."""

    def __init__(self, func: Callable) -> None:
        self._func = func
        self._cache: dict[tuple, Any] = {}

    def __call__(self, *args: Any) -> Any:
        if args not in self._cache:
            self._cache[args] = self._func(*args)
        return self._cache[args]

    def clear_cache(self) -> None:
        self._cache.clear()

    @property
    def cache_size(self) -> int:
        return len(self._cache)


if __name__ == "__main__":
    print("=== Decorator Pattern (class-based) ===")
    processor = BorderDecorator(
        UpperCaseDecorator(TrimDecorator(PlainText())), char="#"
    )
    print(processor.process("  hello world  "))

    print("\n=== Decorator Pattern (function-based) ===")

    @log_calls
    def add(a: int, b: int) -> int:
        return a + b

    add(3, 4)

    print("\n=== Adapter ===")
    legacy = LegacyPrinter()
    modern = PrinterAdapter(legacy)
    print(f"  {modern.print('Hello from adapter!', copies=2)}")

    print("\n=== Lazy Proxy ===")
    proxy = LazyProxy("big_dataset")
    print(f"  Loaded? {proxy.is_loaded}")
    print(f"  Data: {proxy.get_data()}")
    print(f"  Loaded? {proxy.is_loaded}")

    print("\n=== Caching Proxy ===")

    call_count = 0

    def expensive_compute(n: int) -> int:
        global call_count
        call_count += 1
        return n * n

    cached_compute = CachingProxy(expensive_compute)
    print(f"  compute(5) = {cached_compute(5)}")
    print(f"  compute(5) = {cached_compute(5)} (cached)")
    print(f"  compute(10) = {cached_compute(10)}")
    print(f"  Actual function calls: {call_count}")
    print(f"  Cache size: {cached_compute.cache_size}")
