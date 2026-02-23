"""Tests for examples.patterns modules."""

from __future__ import annotations

import pytest

from examples.patterns.creational import (
    DatabaseConnection,
    DarkTheme,
    LightTheme,
    NotificationFactory,
    RequestBuilder,
    get_theme,
)
from examples.patterns.behavioral import (
    CommandHistory,
    DeleteCommand,
    EventEmitter,
    InsertCommand,
    QuickSortStrategy,
    Range2D,
    ReverseSortStrategy,
    Sorter,
    TextEditor,
)
from examples.patterns.structural import (
    BorderDecorator,
    CachingProxy,
    LazyProxy,
    PlainText,
    PrinterAdapter,
    LegacyPrinter,
    TrimDecorator,
    UpperCaseDecorator,
)


class TestCreational:
    def test_singleton(self):
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2

    def test_factory(self):
        email = NotificationFactory.create("email", "test@test.com")
        result = email.send("Hello")
        assert "Email" in result
        assert "test@test.com" in result

    def test_factory_unknown_channel(self):
        with pytest.raises(ValueError, match="Unknown channel"):
            NotificationFactory.create("pigeon", "bird")

    def test_builder(self):
        request = (
            RequestBuilder()
            .method("POST")
            .url("https://api.com/users")
            .header("Content-Type", "application/json")
            .body('{"name":"Alice"}')
            .timeout(10)
            .build()
        )
        assert request.method == "POST"
        assert request.url == "https://api.com/users"
        assert request.headers["Content-Type"] == "application/json"
        assert request.timeout == 10

    def test_builder_missing_url(self):
        with pytest.raises(ValueError, match="URL is required"):
            RequestBuilder().build()

    def test_abstract_factory(self):
        light = get_theme("light")
        assert isinstance(light, LightTheme)
        dark = get_theme("dark")
        assert isinstance(dark, DarkTheme)
        with pytest.raises(ValueError):
            get_theme("neon")


class TestBehavioral:
    def test_event_emitter(self):
        emitter = EventEmitter()
        log: list[str] = []
        emitter.on("click", lambda: log.append("clicked"))
        emitter.emit("click")
        emitter.emit("click")
        assert log == ["clicked", "clicked"]

    def test_event_emitter_off(self):
        emitter = EventEmitter()
        log: list[str] = []
        handler = lambda: log.append("x")  # noqa: E731
        emitter.on("e", handler)
        emitter.emit("e")
        emitter.off("e", handler)
        emitter.emit("e")
        assert log == ["x"]

    def test_strategy(self):
        data = [3, 1, 4, 1, 5]
        sorter = Sorter(QuickSortStrategy())
        assert sorter.sort(data) == [1, 1, 3, 4, 5]
        sorter.strategy = ReverseSortStrategy()
        assert sorter.sort(data) == [5, 4, 3, 1, 1]

    def test_command_insert_undo(self):
        editor = TextEditor()
        history = CommandHistory()
        history.execute(InsertCommand(editor, "Hello"))
        assert editor.content == "Hello"
        history.undo()
        assert editor.content == ""

    def test_command_redo(self):
        editor = TextEditor()
        history = CommandHistory()
        history.execute(InsertCommand(editor, "Hi"))
        history.undo()
        history.redo()
        assert editor.content == "Hi"

    def test_command_delete(self):
        editor = TextEditor(content="Hello World")
        history = CommandHistory()
        history.execute(DeleteCommand(editor, 5, 6))
        assert editor.content == "Hello"
        history.undo()
        assert editor.content == "Hello World"

    def test_range_2d(self):
        pairs = list(Range2D(2, 3))
        assert len(pairs) == 6
        assert pairs[0] == (0, 0)
        assert pairs[-1] == (1, 2)


class TestStructural:
    def test_decorator_chaining(self):
        processor = UpperCaseDecorator(TrimDecorator(PlainText()))
        assert processor.process("  hello  ") == "HELLO"

    def test_border_decorator(self):
        result = BorderDecorator(PlainText(), char="*").process("Hi")
        assert "Hi" in result
        assert "****" in result

    def test_adapter(self):
        legacy = LegacyPrinter()
        modern = PrinterAdapter(legacy)
        result = modern.print("test doc", copies=2)
        assert result.count("[LEGACY]") == 2

    def test_lazy_proxy(self):
        proxy = LazyProxy("test_resource")
        assert proxy.is_loaded is False
        data = proxy.get_data()
        assert proxy.is_loaded is True
        assert "test_resource" in data

    def test_caching_proxy(self):
        call_count = 0

        def compute(n: int) -> int:
            nonlocal call_count
            call_count += 1
            return n * n

        cached = CachingProxy(compute)
        assert cached(5) == 25
        assert cached(5) == 25
        assert call_count == 1
        assert cached.cache_size == 1
