"""Tests for examples.basics modules."""

from __future__ import annotations

import pytest

from examples.basics.variables_and_types import (
    demonstrate_floats,
    demonstrate_integers,
    find_first,
    safe_int,
    string_basics,
    truthy_falsy,
    type_name,
)
from examples.basics.control_flow import (
    chunked,
    classify_number,
    clamp,
    collatz_steps,
    fizzbuzz,
    http_status_message,
    pairwise,
    parse_command,
    read_non_empty,
)
from examples.basics.functions import (
    apply_twice,
    build_url,
    compose,
    flatten,
    flexible_sum,
    greet,
    make_counter,
    make_multiplier,
    memoized_fibonacci,
    multi_return,
    pipeline,
    sort_by_last_char,
    square,
    cube,
)
from examples.basics.strings_and_formatting import (
    build_csv_row,
    extract_emails,
    format_currency,
    is_palindrome,
    slugify,
    title_case,
    truncate,
    word_count,
)
from examples.basics.comprehensions import (
    common_elements,
    evens_only,
    flatten_2d,
    invert_dict,
    matrix_multiply,
    pascal_triangle,
    prime_sieve,
    squares,
    sum_of_squares,
    transpose,
    word_lengths,
)


class TestVariablesAndTypes:
    def test_demonstrate_integers(self):
        result = demonstrate_integers()
        assert result["decimal"] == 42
        assert result["binary"] == 42
        assert result["hex"] == 42
        assert result["power"] == 1764

    def test_demonstrate_floats(self):
        result = demonstrate_floats()
        assert result["rounded"] == 3.14
        assert result["scientific"] == 2500.0

    def test_truthy_falsy(self):
        assert truthy_falsy(1) is True
        assert truthy_falsy(0) is False
        assert truthy_falsy("") is False
        assert truthy_falsy("hello") is True
        assert truthy_falsy([]) is False
        assert truthy_falsy(None) is False

    def test_string_basics(self):
        result = string_basics()
        assert result["upper"] == "HELLO, WORLD!"
        assert result["lower"] == "hello, world!"
        assert result["stripped"] == "spaces"

    def test_safe_int(self):
        assert safe_int("42") == 42
        assert safe_int("nope") == 0
        assert safe_int("nope", -1) == -1

    def test_type_name(self):
        assert type_name(42) == "int"
        assert type_name("hi") == "str"
        assert type_name([]) == "list"

    def test_find_first(self):
        assert find_first([1, 4, 6, 8], lambda x: x > 5) == 6
        assert find_first([1, 2, 3], lambda x: x > 10) is None


class TestControlFlow:
    def test_classify_number(self):
        assert classify_number(5) == "positive"
        assert classify_number(-3) == "negative"
        assert classify_number(0) == "zero"

    def test_clamp(self):
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10

    def test_fizzbuzz(self):
        result = fizzbuzz(15)
        assert result[0] == "1"
        assert result[2] == "Fizz"
        assert result[4] == "Buzz"
        assert result[14] == "FizzBuzz"
        assert len(result) == 15

    def test_collatz_steps(self):
        assert collatz_steps(1) == 0
        assert collatz_steps(6) == 8
        with pytest.raises(ValueError):
            collatz_steps(0)

    def test_pairwise(self):
        assert pairwise([1, 2, 3, 4]) == [(1, 2), (2, 3), (3, 4)]
        assert pairwise([]) == []

    def test_chunked(self):
        assert chunked([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
        assert chunked([], 3) == []

    def test_read_non_empty(self):
        assert read_non_empty(["  hello  ", "", "  ", "world"]) == ["hello", "world"]

    def test_http_status_message(self):
        assert http_status_message(200) == "OK"
        assert http_status_message(404) == "Not Found"
        assert http_status_message(201) == "Success"
        assert http_status_message(999) == "Unknown"

    def test_parse_command(self):
        assert parse_command(["greet", "Alice"]) == "Hello, Alice!"
        assert parse_command(["add", "1", "2", "3"]) == "6"
        assert parse_command(["quit"]) == "Goodbye!"


class TestFunctions:
    def test_greet(self):
        assert greet("Alice") == "Hello, Alice!"
        assert greet("Bob", "Hi") == "Hi, Bob!"

    def test_multi_return(self):
        val, sq, cb = multi_return(3)
        assert (val, sq, cb) == (3, 9, 27)

    def test_flexible_sum(self):
        assert flexible_sum(1, 2, 3) == 6
        assert flexible_sum() == 0

    def test_build_url(self):
        assert build_url("https://api.com") == "https://api.com"
        url = build_url("https://api.com/search", q="python")
        assert "q=python" in url

    def test_apply_twice(self):
        assert apply_twice(lambda x: x * 2, 3) == 12

    def test_compose(self):
        double_then_str = compose(str, lambda x: x * 2)
        assert double_then_str(5) == "10"

    def test_sort_by_last_char(self):
        assert sort_by_last_char(["hello", "world", "abc"]) == ["abc", "world", "hello"]

    def test_make_counter(self):
        counter = make_counter()
        assert counter() == 1
        assert counter() == 2
        assert counter() == 3

    def test_make_multiplier(self):
        double = make_multiplier(2)
        assert double(5) == 10

    def test_pipeline(self):
        transform = pipeline(str.strip, str.lower, str.title)
        assert transform("  hello world  ") == "Hello World"

    def test_square_cube(self):
        assert square(5) == 25
        assert cube(3) == 27

    def test_flatten(self):
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
        assert flatten([]) == []

    def test_memoized_fibonacci(self):
        assert memoized_fibonacci(0) == 0
        assert memoized_fibonacci(1) == 1
        assert memoized_fibonacci(10) == 55


class TestStringsAndFormatting:
    def test_format_currency(self):
        assert format_currency(1234567.89) == "$1,234,567.89"
        assert format_currency(42, "€") == "€42.00"

    def test_is_palindrome(self):
        assert is_palindrome("racecar") is True
        assert is_palindrome("A man a plan a canal Panama") is True
        assert is_palindrome("hello") is False

    def test_title_case(self):
        assert title_case("the lord of the rings") == "The Lord of the Rings"

    def test_truncate(self):
        assert truncate("hello", 10) == "hello"
        assert truncate("hello world", 8) == "hello..."

    def test_word_count(self):
        result = word_count("the cat the cat")
        assert result["the"] == 2
        assert result["cat"] == 2

    def test_extract_emails(self):
        text = "Contact info@test.com and bob@example.org"
        result = extract_emails(text)
        assert "info@test.com" in result
        assert "bob@example.org" in result

    def test_slugify(self):
        assert slugify("Hello, World!") == "hello-world"
        assert slugify("  Multiple   Spaces  ") == "multiple-spaces"

    def test_build_csv_row(self):
        assert build_csv_row("a", "b", "c") == "a,b,c"
        assert '"' in build_csv_row("has, comma")


class TestComprehensions:
    def test_squares(self):
        assert squares(5) == [0, 1, 4, 9, 16]

    def test_evens_only(self):
        assert evens_only([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    def test_flatten_2d(self):
        assert flatten_2d([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_transpose(self):
        assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
        assert transpose([]) == []

    def test_invert_dict(self):
        assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}

    def test_word_lengths(self):
        assert word_lengths(["hi", "hello"]) == {"hi": 2, "hello": 5}

    def test_common_elements(self):
        assert common_elements([1, 2, 3], [2, 3, 4]) == {2, 3}

    def test_sum_of_squares(self):
        assert sum_of_squares(4) == 0 + 1 + 4 + 9

    def test_prime_sieve(self):
        primes = prime_sieve(20)
        assert primes == [2, 3, 5, 7, 11, 13, 17, 19]
        assert prime_sieve(1) == []

    def test_pascal_triangle(self):
        result = pascal_triangle(4)
        assert result == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]

    def test_matrix_multiply(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        assert matrix_multiply(a, b) == [[19, 22], [43, 50]]
