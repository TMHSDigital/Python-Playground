"""Async programming: asyncio, coroutines, and concurrent execution.

asyncio enables concurrent I/O-bound operations using cooperative multitasking.
Unlike threads, async code runs in a single thread and explicitly yields
control with `await`.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator
from dataclasses import dataclass, field


# --- Basic Coroutines ---


async def greet_after(name: str, delay: float) -> str:
    """Greet someone after a delay."""
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


async def fetch_data(url: str, delay: float = 0.1) -> dict:
    """Simulate fetching data from a URL."""
    await asyncio.sleep(delay)
    return {"url": url, "status": 200, "data": f"Response from {url}"}


# --- Concurrent Execution ---


async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently using gather."""
    tasks = [fetch_data(url, delay=0.05) for url in urls]
    return await asyncio.gather(*tasks)


async def fetch_first(urls: list[str]) -> dict:
    """Return the result of whichever URL responds first."""
    tasks = [
        asyncio.create_task(fetch_data(url, delay=i * 0.02))
        for i, url in enumerate(urls)
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return done.pop().result()


# --- Async Context Manager ---


@dataclass
class AsyncConnection:
    """Simulates an async database connection."""

    dsn: str
    _connected: bool = False

    async def __aenter__(self) -> AsyncConnection:
        await asyncio.sleep(0.01)
        self._connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await asyncio.sleep(0.01)
        self._connected = False

    async def query(self, sql: str) -> list[dict]:
        if not self._connected:
            raise RuntimeError("Not connected")
        await asyncio.sleep(0.01)
        return [{"sql": sql, "rows": 42}]

    @property
    def is_connected(self) -> bool:
        return self._connected


# --- Async Iterator ---


class AsyncCounter:
    """An async iterator that counts with delays."""

    def __init__(self, start: int, stop: int, delay: float = 0.01) -> None:
        self.current = start
        self.stop = stop
        self.delay = delay

    def __aiter__(self) -> AsyncIterator[int]:
        return self

    async def __anext__(self) -> int:
        if self.current >= self.stop:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        value = self.current
        self.current += 1
        return value


# --- Async Generator ---


async def async_range(
    start: int, stop: int, delay: float = 0.01
) -> AsyncGenerator[int, None]:
    """An async generator that yields integers with delays."""
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


async def async_filter(predicate, aiterable) -> AsyncGenerator:
    """Filter an async iterable with a predicate."""
    async for item in aiterable:
        if predicate(item):
            yield item


# --- Producer/Consumer with Queue ---


@dataclass
class AsyncWorker:
    """A producer/consumer system using asyncio.Queue."""

    queue: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=10))
    results: list = field(default_factory=list)

    async def produce(self, items: list, delay: float = 0.01) -> None:
        for item in items:
            await asyncio.sleep(delay)
            await self.queue.put(item)
        await self.queue.put(None)

    async def consume(self, worker_id: int) -> None:
        while True:
            item = await self.queue.get()
            if item is None:
                await self.queue.put(None)
                break
            await asyncio.sleep(0.01)
            self.results.append((worker_id, item, item * 2))
            self.queue.task_done()


# --- Semaphore for Rate Limiting ---


async def rate_limited_fetch(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    """Fetch URLs with concurrency limited by a semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def _fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url, delay=0.02)

    tasks = [_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


# --- Timeout ---


async def with_timeout(coro, timeout: float) -> object | None:
    """Run a coroutine with a timeout, returning None on timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return None


# --- Main Demo ---


async def main() -> None:
    print("=== Basic Coroutine ===")
    result = await greet_after("World", 0.01)
    print(f"  {result}")

    print("\n=== Concurrent Fetch ===")
    urls = [f"https://api.example.com/item/{i}" for i in range(5)]
    results = await fetch_all(urls)
    for r in results:
        print(f"  {r['url']} -> {r['status']}")

    print("\n=== First Response ===")
    first = await fetch_first(urls[:3])
    print(f"  First: {first['url']}")

    print("\n=== Async Context Manager ===")
    async with AsyncConnection("postgres://localhost/db") as conn:
        print(f"  Connected: {conn.is_connected}")
        result = await conn.query("SELECT count(*) FROM users")
        print(f"  Query result: {result}")
    print(f"  Connected after exit: {conn.is_connected}")

    print("\n=== Async Iterator ===")
    values = []
    async for val in AsyncCounter(0, 5, delay=0.01):
        values.append(val)
    print(f"  {values}")

    print("\n=== Async Generator ===")
    evens = []
    async for val in async_filter(lambda x: x % 2 == 0, async_range(0, 10, 0.005)):
        evens.append(val)
    print(f"  Evens: {evens}")

    print("\n=== Producer/Consumer ===")
    worker = AsyncWorker()
    await asyncio.gather(
        worker.produce([1, 2, 3, 4, 5]),
        worker.consume(1),
        worker.consume(2),
    )
    print(f"  Results: {sorted(worker.results)}")

    print("\n=== Rate-Limited Fetch ===")
    urls = [f"https://api.example.com/page/{i}" for i in range(6)]
    results = await rate_limited_fetch(urls, max_concurrent=2)
    print(f"  Fetched {len(results)} pages")

    print("\n=== Timeout ===")
    fast = await with_timeout(greet_after("Fast", 0.01), timeout=1.0)
    slow = await with_timeout(greet_after("Slow", 5.0), timeout=0.05)
    print(f"  Fast: {fast}")
    print(f"  Slow: {slow}")


if __name__ == "__main__":
    asyncio.run(main())
