"""Custom data structures: stack, queue, linked list, and binary search tree.

Implementing classic data structures helps understand how Python's built-in
types work under the hood and teaches OOP fundamentals.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


# --- Stack ---


class Stack(Generic[T]):
    """Last-In-First-Out (LIFO) stack."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"


# --- Queue ---


class Queue(Generic[T]):
    """First-In-First-Out (FIFO) queue."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def front(self) -> T:
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({self._items})"


# --- Singly Linked List ---


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T, next_node: _Node[T] | None = None) -> None:
        self.value = value
        self.next = next_node


class LinkedList(Generic[T]):
    """Singly linked list with iteration support."""

    def __init__(self) -> None:
        self._head: _Node[T] | None = None
        self._size: int = 0

    def prepend(self, value: T) -> None:
        self._head = _Node(value, self._head)
        self._size += 1

    def append(self, value: T) -> None:
        new_node = _Node(value)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def remove(self, value: T) -> bool:
        """Remove the first occurrence of value. Returns True if found."""
        if self._head is None:
            return False
        if self._head.value == value:
            self._head = self._head.next
            self._size -= 1
            return True
        current = self._head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def __contains__(self, value: T) -> bool:
        return any(item == value for item in self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        items = " -> ".join(repr(item) for item in self)
        return f"LinkedList({items})"


# --- Binary Search Tree ---


class _BSTNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: int | float) -> None:
        self.key = key
        self.left: _BSTNode | None = None
        self.right: _BSTNode | None = None


class BinarySearchTree:
    """A simple binary search tree supporting insert, search, and traversal."""

    def __init__(self) -> None:
        self._root: _BSTNode | None = None
        self._size: int = 0

    def insert(self, key: int | float) -> None:
        if self._root is None:
            self._root = _BSTNode(key)
            self._size += 1
        else:
            self._insert(self._root, key)

    def _insert(self, node: _BSTNode, key: int | float) -> None:
        if key < node.key:
            if node.left is None:
                node.left = _BSTNode(key)
                self._size += 1
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = _BSTNode(key)
                self._size += 1
            else:
                self._insert(node.right, key)

    def search(self, key: int | float) -> bool:
        return self._search(self._root, key)

    def _search(self, node: _BSTNode | None, key: int | float) -> bool:
        if node is None:
            return False
        if key == node.key:
            return True
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self) -> list[int | float]:
        """Return keys in sorted (inorder) order."""
        result: list[int | float] = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: _BSTNode | None, result: list) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def min_value(self) -> int | float:
        if self._root is None:
            raise ValueError("Tree is empty")
        node = self._root
        while node.left:
            node = node.left
        return node.key

    def max_value(self) -> int | float:
        if self._root is None:
            raise ValueError("Tree is empty")
        node = self._root
        while node.right:
            node = node.right
        return node.key

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: int | float) -> bool:
        return self.search(key)

    def __repr__(self) -> str:
        return f"BinarySearchTree({self.inorder()})"


if __name__ == "__main__":
    print("=== Stack ===")
    stack: Stack[int] = Stack()
    for v in [1, 2, 3]:
        stack.push(v)
    print(f"  {stack}")
    print(f"  pop: {stack.pop()}, peek: {stack.peek()}")

    print("\n=== Queue ===")
    q: Queue[str] = Queue()
    for name in ["Alice", "Bob", "Charlie"]:
        q.enqueue(name)
    print(f"  {q}")
    print(f"  dequeue: {q.dequeue()}, front: {q.front()}")

    print("\n=== LinkedList ===")
    ll: LinkedList[int] = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    print(f"  {ll}")
    ll.remove(3)
    print(f"  after removing 3: {ll}")
    print(f"  4 in list? {4 in ll}")

    print("\n=== BinarySearchTree ===")
    bst = BinarySearchTree()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(v)
    print(f"  {bst}")
    print(f"  search(4): {bst.search(4)}")
    print(f"  search(9): {bst.search(9)}")
    print(f"  min: {bst.min_value()}, max: {bst.max_value()}")
