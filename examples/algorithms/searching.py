"""Searching algorithms: linear search, binary search, and graph traversal.

Covers the most common search patterns with clear complexity analysis.
"""

from __future__ import annotations

from collections import deque
from typing import TypeVar

T = TypeVar("T")


# --- Linear Search ---


def linear_search(arr: list[T], target: T) -> int:
    """Linear Search -- O(n) time, O(1) space.

    Returns the index of target, or -1 if not found.
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1


# --- Binary Search ---


def binary_search(arr: list, target) -> int:
    """Iterative Binary Search -- O(log n) time, O(1) space.

    Requires a sorted array. Returns the index of target, or -1.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def binary_search_recursive(
    arr: list, target, low: int = 0, high: int | None = None
) -> int:
    """Recursive Binary Search -- O(log n) time, O(log n) space (call stack)."""
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


def bisect_left(arr: list, target) -> int:
    """Find the leftmost insertion point for target in a sorted array.

    Equivalent to bisect.bisect_left from the standard library.
    """
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


# --- Graph Search ---

Graph = dict[str, list[str]]


def bfs(graph: Graph, start: str) -> list[str]:
    """Breadth-First Search -- O(V + E) time, O(V) space.

    Returns nodes in BFS order (level by level).
    """
    visited: set[str] = set()
    queue: deque[str] = deque([start])
    order: list[str] = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(n for n in graph.get(node, []) if n not in visited)

    return order


def dfs(graph: Graph, start: str) -> list[str]:
    """Depth-First Search (iterative) -- O(V + E) time, O(V) space."""
    visited: set[str] = set()
    stack: list[str] = [start]
    order: list[str] = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            stack.extend(reversed(graph.get(node, [])))

    return order


def dfs_recursive(
    graph: Graph, start: str, visited: set[str] | None = None
) -> list[str]:
    """Depth-First Search (recursive) -- O(V + E) time, O(V) space."""
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    return order


def shortest_path(graph: Graph, start: str, end: str) -> list[str] | None:
    """Find shortest path using BFS (unweighted graph)."""
    if start == end:
        return [start]

    visited: set[str] = {start}
    queue: deque[list[str]] = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


def has_cycle(graph: Graph) -> bool:
    """Detect if an undirected graph has a cycle using DFS."""
    visited: set[str] = set()

    def _dfs(node: str, parent: str | None) -> bool:
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if _dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in graph:
        if node not in visited:
            if _dfs(node, None):
                return True
    return False


if __name__ == "__main__":
    print("=== Linear Search ===")
    data = [10, 23, 45, 70, 11, 15]
    print(f"  {data}, target=70 -> index {linear_search(data, 70)}")
    print(f"  {data}, target=99 -> index {linear_search(data, 99)}")

    print("\n=== Binary Search ===")
    sorted_data = sorted(data)
    print(f"  {sorted_data}, target=23 -> index {binary_search(sorted_data, 23)}")
    print(f"  {sorted_data}, target=99 -> index {binary_search(sorted_data, 99)}")

    print("\n=== Graph Traversal ===")
    graph: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    print(f"  BFS from A: {bfs(graph, 'A')}")
    print(f"  DFS from A: {dfs(graph, 'A')}")

    print("\n=== Shortest Path ===")
    path = shortest_path(graph, "A", "F")
    print(f"  A -> F: {' -> '.join(path) if path else 'No path'}")
