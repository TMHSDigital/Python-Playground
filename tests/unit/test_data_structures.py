"""Tests for examples.data_structures modules."""

from __future__ import annotations

import pytest

from examples.data_structures.collections_guide import (
    are_anagrams,
    deduplicate_preserve_order,
    deep_get,
    distance,
    group_anagrams,
    interleave,
    jaccard_similarity,
    merge_dicts,
    most_common_words,
    Point,
    rotate_list,
    sliding_window_max,
)
from examples.data_structures.dataclasses_guide import (
    Color,
    Config,
    Coordinate,
    Version,
    Vector3D,
)
from examples.data_structures.custom_structures import (
    BinarySearchTree,
    LinkedList,
    Queue,
    Stack,
)


class TestCollections:
    def test_rotate_list(self):
        assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
        assert rotate_list([], 5) == []

    def test_interleave(self):
        assert interleave([1, 2, 3], ["a", "b", "c"]) == [1, "a", 2, "b", 3, "c"]

    def test_deduplicate_preserve_order(self):
        assert deduplicate_preserve_order([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [
            3,
            1,
            4,
            5,
            9,
            2,
            6,
        ]

    def test_named_tuple_distance(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert distance(p1, p2) == 5.0

    def test_merge_dicts(self):
        result = merge_dicts({"a": 1}, {"b": 2}, {"a": 3})
        assert result == {"a": 3, "b": 2}

    def test_deep_get(self):
        data = {"user": {"profile": {"name": "Alice"}}}
        assert deep_get(data, ["user", "profile", "name"]) == "Alice"
        assert deep_get(data, ["user", "missing"], "N/A") == "N/A"

    def test_group_anagrams(self):
        result = group_anagrams(["eat", "tea", "ate"])
        assert len(result) == 1
        assert sorted(result[0]) == ["ate", "eat", "tea"]

    def test_most_common_words(self):
        result = most_common_words("a a a b b c", 2)
        assert result[0] == ("a", 3)
        assert result[1] == ("b", 2)

    def test_are_anagrams(self):
        assert are_anagrams("listen", "silent") is True
        assert are_anagrams("hello", "world") is False

    def test_sliding_window_max(self):
        assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
        assert sliding_window_max([], 3) == []

    def test_jaccard_similarity(self):
        assert jaccard_similarity({1, 2, 3}, {2, 3, 4}) == pytest.approx(0.5)
        assert jaccard_similarity(set(), set()) == 1.0


class TestDataclasses:
    def test_coordinate_distance(self):
        a = Coordinate(0, 0)
        b = Coordinate(3, 4)
        assert a.distance_to(b) == 5.0

    def test_config_defaults(self):
        cfg = Config()
        assert cfg.host == "localhost"
        assert cfg.port == 8080
        assert cfg.tags == []

    def test_config_base_url(self):
        cfg = Config(host="api.com", port=443)
        assert cfg.base_url() == "https://api.com:443"

    def test_color_frozen(self):
        c = Color(255, 0, 0)
        assert c.hex() == "#ff0000"
        with pytest.raises(AttributeError):
            c.r = 100  # type: ignore[misc]

    def test_color_from_hex(self):
        c = Color.from_hex("#00ff00")
        assert c == Color(0, 255, 0)

    def test_version_ordering(self):
        versions = [Version(2, 0, 0), Version(1, 9, 1), Version(1, 10, 0)]
        sorted_v = sorted(versions)
        assert str(sorted_v[0]) == "1.9.1"
        assert str(sorted_v[1]) == "1.10.0"
        assert str(sorted_v[2]) == "2.0.0"

    def test_vector3d(self):
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(0, 1, 0)
        cross = v1.cross(v2)
        assert cross == Vector3D(0, 0, 1)
        assert v1.dot(v2) == 0
        assert v1.magnitude() == 1.0


class TestStack:
    def test_push_pop(self):
        s: Stack[int] = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s: Stack[str] = Stack()
        s.push("hello")
        assert s.peek() == "hello"
        assert len(s) == 1

    def test_empty_pop_raises(self):
        s: Stack[int] = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_is_empty(self):
        s: Stack[int] = Stack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()


class TestQueue:
    def test_enqueue_dequeue(self):
        q: Queue[int] = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert q.dequeue() == 2

    def test_front(self):
        q: Queue[str] = Queue()
        q.enqueue("first")
        assert q.front() == "first"
        assert len(q) == 1

    def test_empty_dequeue_raises(self):
        q: Queue[int] = Queue()
        with pytest.raises(IndexError):
            q.dequeue()


class TestLinkedList:
    def test_append_and_iterate(self):
        ll: LinkedList[int] = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert list(ll) == [1, 2, 3]

    def test_prepend(self):
        ll: LinkedList[int] = LinkedList()
        ll.prepend(3)
        ll.prepend(2)
        ll.prepend(1)
        assert list(ll) == [1, 2, 3]

    def test_remove(self):
        ll: LinkedList[int] = LinkedList()
        for v in [1, 2, 3]:
            ll.append(v)
        assert ll.remove(2) is True
        assert list(ll) == [1, 3]
        assert ll.remove(99) is False

    def test_contains(self):
        ll: LinkedList[int] = LinkedList()
        ll.append(42)
        assert 42 in ll
        assert 99 not in ll

    def test_len(self):
        ll: LinkedList[int] = LinkedList()
        assert len(ll) == 0
        ll.append(1)
        ll.append(2)
        assert len(ll) == 2


class TestBST:
    def test_insert_and_search(self):
        bst = BinarySearchTree()
        for v in [5, 3, 7, 1, 4]:
            bst.insert(v)
        assert bst.search(3) is True
        assert bst.search(9) is False
        assert 3 in bst

    def test_inorder(self):
        bst = BinarySearchTree()
        for v in [5, 3, 7, 1, 4, 6, 8]:
            bst.insert(v)
        assert bst.inorder() == [1, 3, 4, 5, 6, 7, 8]

    def test_min_max(self):
        bst = BinarySearchTree()
        for v in [5, 3, 7, 1, 9]:
            bst.insert(v)
        assert bst.min_value() == 1
        assert bst.max_value() == 9

    def test_empty_raises(self):
        bst = BinarySearchTree()
        with pytest.raises(ValueError):
            bst.min_value()

    def test_len(self):
        bst = BinarySearchTree()
        assert len(bst) == 0
        bst.insert(5)
        bst.insert(3)
        bst.insert(5)  # duplicate, should not increase size
        assert len(bst) == 2
