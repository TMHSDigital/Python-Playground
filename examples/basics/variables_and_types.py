"""Variables, data types, and type conversions in Python.

Python is dynamically typed -- variables don't need explicit type declarations.
This module demonstrates the fundamental built-in types and how to work with them.
"""

from __future__ import annotations


# --- Numeric Types ---


def demonstrate_integers() -> dict[str, int]:
    """Show integer operations and useful built-in functions."""
    x = 42
    binary = 0b101010  # 42 in binary
    hexval = 0x2A  # 42 in hex
    octal = 0o52  # 42 in octal

    return {
        "decimal": x,
        "binary": binary,
        "hex": hexval,
        "octal": octal,
        "power": x**2,
        "floor_div": x // 5,
        "modulo": x % 5,
        "abs": abs(-x),
    }


def demonstrate_floats() -> dict[str, float]:
    """Show floating-point behavior and common pitfalls."""
    pi = 3.14159
    scientific = 2.5e3  # 2500.0

    return {
        "pi": pi,
        "scientific": scientific,
        "rounded": round(pi, 2),
        "precision_issue": 0.1 + 0.2,  # ≈ 0.30000000000000004
    }


# --- Boolean Type ---


def truthy_falsy(value: object) -> bool:
    """Demonstrate Python's truthiness rules.

    Falsy values: None, False, 0, 0.0, '', [], {}, set(), frozenset()
    Everything else is truthy.
    """
    return bool(value)


# --- String Type ---


def string_basics() -> dict[str, str]:
    """Common string operations."""
    greeting = "Hello, World!"
    return {
        "upper": greeting.upper(),
        "lower": greeting.lower(),
        "title": greeting.title(),
        "stripped": "  spaces  ".strip(),
        "replaced": greeting.replace("World", "Python"),
        "split_first": greeting.split(",")[0],
        "reversed": greeting[::-1],
    }


# --- Type Conversions ---


def safe_int(value: str, default: int = 0) -> int:
    """Convert a string to int with a fallback default."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def type_name(value: object) -> str:
    """Return the type name of any object."""
    return type(value).__name__


# --- None Type ---


def find_first(items: list, predicate) -> object | None:
    """Return the first item matching predicate, or None."""
    for item in items:
        if predicate(item):
            return item
    return None


if __name__ == "__main__":
    print("=== Integers ===")
    for k, v in demonstrate_integers().items():
        print(f"  {k}: {v}")

    print("\n=== Floats ===")
    for k, v in demonstrate_floats().items():
        print(f"  {k}: {v}")

    print("\n=== Truthiness ===")
    for val in [0, 1, "", "hello", [], [1], None, True]:
        print(f"  {val!r:>10} -> {truthy_falsy(val)}")

    print("\n=== Strings ===")
    for k, v in string_basics().items():
        print(f"  {k}: {v!r}")

    print(f"\n=== safe_int ===")
    print(f"  '42'   -> {safe_int('42')}")
    print(f"  'nope' -> {safe_int('nope', -1)}")

    print(f"\n=== find_first ===")
    result = find_first([1, 4, 6, 8, 3], lambda x: x > 5)
    print(f"  First > 5 in [1,4,6,8,3]: {result}")
