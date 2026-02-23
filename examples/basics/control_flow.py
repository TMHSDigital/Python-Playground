"""Control flow: conditionals, loops, match statements, and iteration patterns.

Covers if/elif/else, for/while loops, the walrus operator, and
structural pattern matching (Python 3.10+).
"""

from __future__ import annotations

from collections.abc import Iterator


# --- Conditionals ---


def classify_number(n: int | float) -> str:
    """Classify a number as positive, negative, or zero."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


def clamp(value: float, lo: float, hi: float) -> float:
    """Constrain a value to [lo, hi] range."""
    return max(lo, min(hi, value))


# --- Ternary / Conditional Expression ---


def absolute(n: int | float) -> int | float:
    """Absolute value using a conditional expression."""
    return n if n >= 0 else -n


# --- Loops ---


def fizzbuzz(n: int) -> list[str]:
    """Classic FizzBuzz for 1..n."""
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


def collatz_steps(n: int) -> int:
    """Count steps to reach 1 in the Collatz sequence."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


# --- Iteration Patterns ---


def enumerate_pairs(items: list) -> list[tuple[int, object]]:
    """Demonstrate enumerate for index-value pairs."""
    return list(enumerate(items))


def pairwise(items: list) -> list[tuple]:
    """Yield consecutive pairs from a sequence."""
    return list(zip(items, items[1:]))


def chunked(items: list, size: int) -> list[list]:
    """Split a list into chunks of the given size."""
    return [items[i : i + size] for i in range(0, len(items), size)]


# --- Walrus Operator (Python 3.8+) ---


def read_non_empty(lines: list[str]) -> list[str]:
    """Filter and strip lines, keeping only non-empty ones.

    Demonstrates the walrus operator `:=` to avoid repeated computation.
    """
    return [stripped for line in lines if (stripped := line.strip())]


# --- Structural Pattern Matching (Python 3.10+) ---


def http_status_message(code: int) -> str:
    """Return a human-readable message for an HTTP status code."""
    match code:
        case 200:
            return "OK"
        case 301:
            return "Moved Permanently"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _ if 200 <= code < 300:
            return "Success"
        case _ if 400 <= code < 500:
            return "Client Error"
        case _ if 500 <= code < 600:
            return "Server Error"
        case _:
            return "Unknown"


def parse_command(command: list[str]) -> str:
    """Parse a CLI-style command using pattern matching."""
    match command:
        case ["quit" | "exit"]:
            return "Goodbye!"
        case ["greet", name]:
            return f"Hello, {name}!"
        case ["add", *numbers] if numbers:
            return str(sum(int(n) for n in numbers))
        case [cmd, *_]:
            return f"Unknown command: {cmd}"
        case _:
            return "Empty command"


# --- For/Else ---


def find_prime_factor(n: int) -> int | None:
    """Find the smallest prime factor, demonstrating for/else."""
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i
    else:
        return None if n < 2 else n  # n itself is prime


# --- Infinite Iterator with Break ---


def countdown(start: int) -> Iterator[int]:
    """Generate a countdown from start to 0."""
    while start >= 0:
        yield start
        start -= 1


if __name__ == "__main__":
    print("=== classify_number ===")
    for val in [-5, 0, 3.14]:
        print(f"  {val} -> {classify_number(val)}")

    print("\n=== FizzBuzz (1-20) ===")
    print("  " + ", ".join(fizzbuzz(20)))

    print("\n=== Collatz steps ===")
    for n in [1, 6, 27]:
        print(f"  {n} -> {collatz_steps(n)} steps")

    print("\n=== Pattern Matching ===")
    for code in [200, 301, 404, 418, 500]:
        print(f"  {code} -> {http_status_message(code)}")

    print("\n=== parse_command ===")
    for cmd in [["greet", "Alice"], ["add", "1", "2", "3"], ["quit"], ["???"]]:
        print(f"  {cmd} -> {parse_command(cmd)}")

    print("\n=== chunked ===")
    print(f"  {chunked(list(range(10)), 3)}")
