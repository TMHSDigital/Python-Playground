"""Context managers: resource management and the `with` statement.

Context managers ensure cleanup code runs even if exceptions occur.
They're used for files, locks, database connections, and more.
"""

from __future__ import annotations

import time
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


# --- Class-based Context Manager ---


class Timer:
    """Measure elapsed time within a `with` block.

    Usage:
        with Timer("my_operation") as t:
            do_stuff()
        print(t.elapsed)
    """

    def __init__(self, label: str = "Timer") -> None:
        self.label = label
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> Timer:
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.elapsed = time.perf_counter() - self._start
        print(f"  [{self.label}] {self.elapsed:.6f}s")
        return False


class TempDirectory:
    """Create and clean up a temporary directory.

    Simulates resource lifecycle management.
    """

    def __init__(self, prefix: str = "tmp") -> None:
        self.prefix = prefix
        self.path: str = ""
        self._files: list[str] = []

    def __enter__(self) -> TempDirectory:
        self.path = f"/tmp/{self.prefix}_{id(self)}"
        return self

    def add_file(self, name: str) -> str:
        filepath = f"{self.path}/{name}"
        self._files.append(filepath)
        return filepath

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        for f in self._files:
            pass  # would delete files in real impl
        self._files.clear()
        self.path = ""
        return False


class ErrorSuppressor:
    """Suppress specified exception types within a block."""

    def __init__(self, *exceptions: type[BaseException]) -> None:
        self.exceptions = exceptions
        self.exception: BaseException | None = None

    def __enter__(self) -> ErrorSuppressor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type and issubclass(exc_type, self.exceptions):
            self.exception = exc_val
            return True
        return False


# --- Generator-based Context Managers ---


@contextmanager
def managed_resource(name: str) -> Generator[dict[str, Any], None, None]:
    """Simulates acquiring and releasing a resource."""
    resource = {"name": name, "status": "acquired", "data": []}
    print(f"  Acquiring resource: {name}")
    try:
        yield resource
    except Exception as e:
        resource["status"] = "error"
        print(f"  Error in resource {name}: {e}")
        raise
    finally:
        resource["status"] = "released"
        print(f"  Released resource: {name}")


@contextmanager
def transaction(name: str = "tx") -> Generator[list, None, None]:
    """Simulates a database transaction with rollback on error."""
    operations: list[str] = []
    print(f"  BEGIN {name}")
    try:
        yield operations
        print(f"  COMMIT {name} ({len(operations)} operations)")
    except Exception as e:
        print(f"  ROLLBACK {name}: {e}")
        operations.clear()
        raise


@contextmanager
def indent_printer(level: int = 1, char: str = "  ") -> Generator[Any, None, None]:
    """Context manager that provides an indented print function."""
    prefix = char * level

    class IndentedPrinter:
        @staticmethod
        def print(*args: Any) -> None:
            print(prefix, *args)

    yield IndentedPrinter()


# --- Reentrant Context Manager ---


@dataclass
class ConnectionPool:
    """A connection pool that tracks active connections.

    Supports reentrant usage (nested `with` blocks).
    """

    max_size: int = 5
    _active: list[str] = field(default_factory=list)
    _count: int = 0

    @contextmanager
    def connection(self, label: str = "") -> Generator[str, None, None]:
        if len(self._active) >= self.max_size:
            raise RuntimeError("Connection pool exhausted")
        self._count += 1
        conn_id = label or f"conn_{self._count}"
        self._active.append(conn_id)
        try:
            yield conn_id
        finally:
            self._active.remove(conn_id)

    @property
    def active_count(self) -> int:
        return len(self._active)


# --- Multiple Context Managers ---


def demonstrate_multiple_managers() -> None:
    """Using multiple context managers with a single `with` statement."""
    with Timer("outer"), ErrorSuppressor(ValueError):
        time.sleep(0.01)
        print("  Inside multiple managers")


if __name__ == "__main__":
    print("=== Timer ===")
    with Timer("sleep_test"):
        time.sleep(0.02)

    print("\n=== TempDirectory ===")
    with TempDirectory("myapp") as tmpdir:
        f1 = tmpdir.add_file("data.csv")
        f2 = tmpdir.add_file("config.json")
        print(f"  Created: {f1}, {f2}")
    print(f"  After exit: path={tmpdir.path!r}, files={tmpdir._files}")

    print("\n=== ErrorSuppressor ===")
    with ErrorSuppressor(ZeroDivisionError) as ctx:
        result = 1 / 0
    print(f"  Suppressed: {ctx.exception}")

    print("\n=== managed_resource ===")
    with managed_resource("database") as db:
        db["data"].append("record1")
        print(f"  Resource data: {db['data']}")

    print("\n=== transaction ===")
    with transaction("insert_users") as ops:
        ops.append("INSERT user1")
        ops.append("INSERT user2")

    print("\n=== ConnectionPool ===")
    pool = ConnectionPool(max_size=3)
    with pool.connection("db") as c1:
        with pool.connection("cache") as c2:
            print(f"  Active: {pool.active_count} ({c1}, {c2})")
    print(f"  After exit: {pool.active_count} active")

    print("\n=== indent_printer ===")
    with indent_printer(2) as p:
        p.print("Indented output")
        p.print("More indented output")
