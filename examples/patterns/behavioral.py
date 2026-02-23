"""Behavioral design patterns: Observer, Strategy, and Command.

Behavioral patterns deal with communication between objects and
assignment of responsibilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


# --- Observer Pattern ---


class EventEmitter:
    """A simple publish/subscribe event system.

    This Pythonic approach uses callbacks rather than the classic
    Observer interface, which is more idiomatic.
    """

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback: Callable) -> None:
        if event in self._listeners:
            self._listeners[event] = [
                cb for cb in self._listeners[event] if cb is not callback
            ]

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


# --- Strategy Pattern ---


class SortStrategy(ABC):
    """Abstract sorting strategy."""

    @abstractmethod
    def sort(self, data: list) -> list: ...


class QuickSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data)  # Python's Timsort as a stand-in


class ReverseSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, reverse=True)


class StableSortByKeyStrategy(SortStrategy):
    def __init__(self, key: Callable) -> None:
        self.key = key

    def sort(self, data: list) -> list:
        return sorted(data, key=self.key)


@dataclass
class Sorter:
    """Context that uses a pluggable sorting strategy."""

    strategy: SortStrategy

    def sort(self, data: list) -> list:
        return self.strategy.sort(data)


# Pythonic alternative: just pass functions
def sort_with(data: list, strategy: Callable[[list], list]) -> list:
    """Functional approach to the Strategy pattern."""
    return strategy(data)


# --- Command Pattern ---


class Command(ABC):
    """Abstract command with undo support."""

    @abstractmethod
    def execute(self) -> str: ...

    @abstractmethod
    def undo(self) -> str: ...


@dataclass
class TextEditor:
    """A simple text editor that commands operate on."""

    content: str = ""

    def insert(self, text: str, position: int | None = None) -> None:
        if position is None:
            self.content += text
        else:
            self.content = self.content[:position] + text + self.content[position:]

    def delete(self, start: int, length: int) -> str:
        deleted = self.content[start : start + length]
        self.content = self.content[:start] + self.content[start + length :]
        return deleted


class InsertCommand(Command):
    def __init__(
        self, editor: TextEditor, text: str, position: int | None = None
    ) -> None:
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self) -> str:
        self.position = (
            self.position if self.position is not None else len(self.editor.content)
        )
        self.editor.insert(self.text, self.position)
        return f"Inserted '{self.text}' at position {self.position}"

    def undo(self) -> str:
        assert self.position is not None
        self.editor.delete(self.position, len(self.text))
        return f"Undid insert of '{self.text}'"


class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, length: int) -> None:
        self.editor = editor
        self.start = start
        self.length = length
        self._deleted_text: str = ""

    def execute(self) -> str:
        self._deleted_text = self.editor.delete(self.start, self.length)
        return f"Deleted '{self._deleted_text}' at position {self.start}"

    def undo(self) -> str:
        self.editor.insert(self._deleted_text, self.start)
        return f"Undid delete, restored '{self._deleted_text}'"


@dataclass
class CommandHistory:
    """Manages command execution with undo/redo support."""

    _history: list[Command] = field(default_factory=list)
    _redo_stack: list[Command] = field(default_factory=list)

    def execute(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()
        return result

    def undo(self) -> str:
        if not self._history:
            return "Nothing to undo"
        command = self._history.pop()
        result = command.undo()
        self._redo_stack.append(command)
        return result

    def redo(self) -> str:
        if not self._redo_stack:
            return "Nothing to redo"
        command = self._redo_stack.pop()
        result = command.execute()
        self._history.append(command)
        return result


# --- Iterator Pattern (Python's protocol) ---


@dataclass
class Range2D:
    """Iterate over all (x, y) pairs in a 2D grid.

    Demonstrates implementing the iterator protocol.
    """

    rows: int
    cols: int

    def __iter__(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield (r, c)


if __name__ == "__main__":
    print("=== Observer (EventEmitter) ===")
    emitter = EventEmitter()
    log: list[str] = []
    emitter.on("user:login", lambda name: log.append(f"User logged in: {name}"))
    emitter.on("user:login", lambda name: log.append(f"Welcome back, {name}!"))
    emitter.emit("user:login", "Alice")
    for entry in log:
        print(f"  {entry}")

    print("\n=== Strategy ===")
    data = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
    sorter = Sorter(StableSortByKeyStrategy(key=lambda x: x[1]))
    print(f"  By age: {sorter.sort(data)}")
    sorter.strategy = ReverseSortStrategy()
    print(f"  Reverse: {sorter.sort(data)}")

    print("\n=== Command (TextEditor) ===")
    editor = TextEditor()
    history = CommandHistory()
    print(f"  {history.execute(InsertCommand(editor, 'Hello'))}")
    print(f"  {history.execute(InsertCommand(editor, ' World'))}")
    print(f"  Content: '{editor.content}'")
    print(f"  {history.undo()}")
    print(f"  Content: '{editor.content}'")
    print(f"  {history.redo()}")
    print(f"  Content: '{editor.content}'")
    print(f"  {history.execute(DeleteCommand(editor, 0, 5))}")
    print(f"  Content: '{editor.content}'")
    print(f"  {history.undo()}")
    print(f"  Content: '{editor.content}'")

    print("\n=== Range2D ===")
    grid = list(Range2D(2, 3))
    print(f"  2x3 grid: {grid}")
