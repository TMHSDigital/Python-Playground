"""Tests for examples.algorithms modules."""

from __future__ import annotations

import pytest

from examples.algorithms.sorting import (
    bubble_sort,
    counting_sort,
    insertion_sort,
    is_sorted,
    merge_sort,
    quicksort,
    selection_sort,
)
from examples.algorithms.searching import (
    bfs,
    binary_search,
    bisect_left,
    dfs,
    has_cycle,
    linear_search,
    shortest_path,
)
from examples.algorithms.recursion import (
    coin_change,
    factorial,
    fibonacci,
    gcd,
    longest_common_subsequence,
    max_subarray_sum,
    n_queens,
    permutations,
    power,
    subsets,
    tower_of_hanoi,
)


class TestSorting:
    UNSORTED = [64, 34, 25, 12, 22, 11, 90]
    EXPECTED = [11, 12, 22, 25, 34, 64, 90]

    @pytest.mark.parametrize(
        "sort_func",
        [
            bubble_sort,
            insertion_sort,
            selection_sort,
            merge_sort,
            quicksort,
        ],
    )
    def test_sort_algorithms(self, sort_func):
        result = sort_func(self.UNSORTED)
        assert result == self.EXPECTED
        assert self.UNSORTED != self.EXPECTED  # original unchanged

    @pytest.mark.parametrize(
        "sort_func",
        [
            bubble_sort,
            insertion_sort,
            selection_sort,
            merge_sort,
            quicksort,
        ],
    )
    def test_sort_empty(self, sort_func):
        assert sort_func([]) == []

    @pytest.mark.parametrize(
        "sort_func",
        [
            bubble_sort,
            insertion_sort,
            selection_sort,
            merge_sort,
            quicksort,
        ],
    )
    def test_sort_single(self, sort_func):
        assert sort_func([1]) == [1]

    @pytest.mark.parametrize(
        "sort_func",
        [
            bubble_sort,
            insertion_sort,
            selection_sort,
            merge_sort,
            quicksort,
        ],
    )
    def test_sort_already_sorted(self, sort_func):
        data = [1, 2, 3, 4, 5]
        assert sort_func(data) == data

    def test_counting_sort(self):
        assert counting_sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]
        assert counting_sort([]) == []

    def test_is_sorted(self):
        assert is_sorted([1, 2, 3, 4]) is True
        assert is_sorted([1, 3, 2]) is False
        assert is_sorted([]) is True


class TestSearching:
    def test_linear_search(self):
        data = [10, 23, 45, 70, 11]
        assert linear_search(data, 70) == 3
        assert linear_search(data, 99) == -1

    def test_binary_search(self):
        data = [10, 11, 23, 45, 70]
        assert binary_search(data, 23) == 2
        assert binary_search(data, 99) == -1

    def test_bisect_left(self):
        data = [1, 3, 3, 5, 7]
        assert bisect_left(data, 3) == 1
        assert bisect_left(data, 4) == 3
        assert bisect_left(data, 0) == 0

    def test_bfs(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
        result = bfs(graph, "A")
        assert result[0] == "A"
        assert set(result) == {"A", "B", "C", "D"}

    def test_dfs(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
        result = dfs(graph, "A")
        assert result[0] == "A"
        assert set(result) == {"A", "B", "C", "D"}

    def test_shortest_path(self):
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        path = shortest_path(graph, "A", "D")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "D"
        assert len(path) == 3

    def test_shortest_path_no_route(self):
        graph = {"A": ["B"], "B": [], "C": []}
        assert shortest_path(graph, "A", "C") is None

    def test_has_cycle(self):
        acyclic = {"A": ["B"], "B": ["C"], "C": []}
        cyclic = {"A": ["B"], "B": ["C"], "C": ["A"]}
        assert has_cycle(acyclic) is False
        assert has_cycle(cyclic) is True


class TestRecursion:
    def test_factorial(self):
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        with pytest.raises(ValueError):
            factorial(-1)

    def test_fibonacci(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55

    def test_gcd(self):
        assert gcd(48, 18) == 6
        assert gcd(0, 5) == 5
        assert gcd(-12, 8) == 4

    def test_power(self):
        assert power(2, 10) == 1024
        assert power(3, 0) == 1
        assert power(2, -2) == pytest.approx(0.25)

    def test_max_subarray_sum(self):
        assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
        assert max_subarray_sum([]) == 0

    def test_permutations(self):
        result = permutations([1, 2, 3])
        assert len(result) == 6
        assert [1, 2, 3] in result
        assert [3, 2, 1] in result

    def test_n_queens(self):
        solutions = n_queens(4)
        assert len(solutions) == 2
        solutions_8 = n_queens(8)
        assert len(solutions_8) == 92

    def test_subsets(self):
        result = subsets([1, 2])
        assert len(result) == 4
        assert [] in result
        assert [1, 2] in result

    def test_coin_change(self):
        assert coin_change([1, 5, 10, 25], 30) == 2  # 25 + 5
        assert coin_change([2], 3) == -1

    def test_lcs(self):
        result = longest_common_subsequence("ABCBDAB", "BDCAB")
        assert len(result) == 4  # multiple valid LCS exist

    def test_tower_of_hanoi(self):
        moves = tower_of_hanoi(3)
        assert len(moves) == 7  # 2^n - 1
