"""String operations, formatting, and regular expressions.

Covers f-strings, format specs, template strings, regex basics,
and common string processing patterns.
"""

from __future__ import annotations

import re
import textwrap


# --- F-String Formatting ---


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a number as currency with commas and two decimal places."""
    return f"{symbol}{amount:,.2f}"


def format_table_row(name: str, value: float, width: int = 20) -> str:
    """Format a name-value pair as an aligned table row."""
    return f"{name:<{width}} {value:>10.2f}"


def format_binary(n: int) -> str:
    """Show an integer in decimal, hex, octal, and binary."""
    return f"dec={n}, hex={n:#x}, oct={n:#o}, bin={n:#b}"


# --- String Methods ---


def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome (ignoring case and spaces)."""
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    return cleaned == cleaned[::-1]


def title_case(text: str) -> str:
    """Convert to title case, handling apostrophes correctly."""
    minor_words = {
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "for",
        "nor",
        "in",
        "on",
        "at",
        "to",
        "by",
        "of",
        "up",
    }
    words = text.lower().split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word not in minor_words:
            result.append(word.capitalize())
        else:
            result.append(word)
    return " ".join(result)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def word_count(text: str) -> dict[str, int]:
    """Count word frequencies in text (case-insensitive)."""
    words = re.findall(r"\b\w+\b", text.lower())
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


# --- Regular Expressions ---


def extract_emails(text: str) -> list[str]:
    """Extract all email addresses from text."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def extract_urls(text: str) -> list[str]:
    """Extract HTTP/HTTPS URLs from text."""
    pattern = r"https?://[^\s<>\"')\]]+"
    return re.findall(pattern, text)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def mask_sensitive(text: str, pattern: str = r"\b\d{4}\b") -> str:
    """Replace matches of a pattern with asterisks."""
    return re.sub(pattern, "****", text)


# --- Multi-line Strings ---


def dedented_block(text: str) -> str:
    """Remove common leading whitespace from a multi-line string."""
    return textwrap.dedent(text).strip()


def wrap_paragraph(text: str, width: int = 72) -> str:
    """Wrap text to the specified width."""
    return textwrap.fill(text, width=width)


# --- String Building ---


def build_csv_row(*values: object) -> str:
    """Build a CSV row, quoting values that contain commas."""
    parts = []
    for v in values:
        s = str(v)
        if "," in s or '"' in s:
            s = '"' + s.replace('"', '""') + '"'
        parts.append(s)
    return ",".join(parts)


def repeat_pattern(pattern: str, count: int, separator: str = " ") -> str:
    """Repeat a pattern with a separator."""
    return separator.join([pattern] * count)


if __name__ == "__main__":
    print("=== Currency ===")
    print(f"  {format_currency(1234567.89)}")
    print(f"  {format_currency(42, '€')}")

    print("\n=== Table Row ===")
    print(f"  {format_table_row('Revenue', 1234567.89)}")
    print(f"  {format_table_row('Expenses', 987654.32)}")

    print("\n=== Palindrome ===")
    for s in ["racecar", "A man a plan a canal Panama", "hello"]:
        print(f"  {s!r:>40} -> {is_palindrome(s)}")

    print("\n=== Title Case ===")
    print(f"  {title_case('the lord of the rings')!r}")

    print("\n=== Slugify ===")
    print(f"  {slugify('Hello, World! This is a TEST.')!r}")

    print("\n=== Extract Emails ===")
    text = "Contact us at info@example.com or support@test.org"
    print(f"  {extract_emails(text)}")

    print("\n=== Word Count ===")
    print(f"  {word_count('the cat sat on the mat the cat')}")

    print("\n=== CSV Row ===")
    print(f"  {build_csv_row('Alice', 30, 'New York, NY')}")
