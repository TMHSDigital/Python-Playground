"""Creational design patterns: Singleton, Factory, and Builder.

Creational patterns deal with object creation mechanisms, trying to create
objects in a manner suitable to the situation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar


# --- Singleton ---


class Singleton:
    """Ensure a class has only one instance using __new__.

    Thread-safe version would use threading.Lock.
    """

    _instance: ClassVar[Singleton | None] = None

    def __new__(cls) -> Singleton:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class DatabaseConnection(Singleton):
    """Example singleton: a database connection pool."""

    _initialized: bool = False

    def __init__(self) -> None:
        if not self._initialized:
            self.connections: list[str] = []
            self._initialized = True

    def connect(self, dsn: str) -> str:
        self.connections.append(dsn)
        return f"Connected to {dsn}"

    def active_connections(self) -> int:
        return len(self.connections)


# --- Factory Method ---


class Notification(ABC):
    """Abstract notification interface."""

    @abstractmethod
    def send(self, message: str) -> str: ...


class EmailNotification(Notification):
    def __init__(self, to: str) -> None:
        self.to = to

    def send(self, message: str) -> str:
        return f"Email to {self.to}: {message}"


class SMSNotification(Notification):
    def __init__(self, phone: str) -> None:
        self.phone = phone

    def send(self, message: str) -> str:
        return f"SMS to {self.phone}: {message}"


class PushNotification(Notification):
    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def send(self, message: str) -> str:
        return f"Push to {self.device_id}: {message}"


class NotificationFactory:
    """Factory that creates the appropriate notification type."""

    _registry: ClassVar[dict[str, type[Notification]]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, channel: str, target: str) -> Notification:
        klass = cls._registry.get(channel)
        if klass is None:
            raise ValueError(f"Unknown channel: {channel}")
        return klass(target)

    @classmethod
    def register(cls, channel: str, klass: type[Notification]) -> None:
        """Extend the factory with new notification types."""
        cls._registry[channel] = klass


# --- Builder ---


@dataclass
class HTTPRequest:
    """An HTTP request built using the builder pattern."""

    method: str = "GET"
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None
    timeout: int = 30
    params: dict[str, str] = field(default_factory=dict)


class RequestBuilder:
    """Fluent builder for constructing HTTPRequest objects."""

    def __init__(self) -> None:
        self._request = HTTPRequest()

    def method(self, method: str) -> RequestBuilder:
        self._request.method = method.upper()
        return self

    def url(self, url: str) -> RequestBuilder:
        self._request.url = url
        return self

    def header(self, key: str, value: str) -> RequestBuilder:
        self._request.headers[key] = value
        return self

    def body(self, body: str) -> RequestBuilder:
        self._request.body = body
        return self

    def timeout(self, seconds: int) -> RequestBuilder:
        self._request.timeout = seconds
        return self

    def param(self, key: str, value: str) -> RequestBuilder:
        self._request.params[key] = value
        return self

    def build(self) -> HTTPRequest:
        if not self._request.url:
            raise ValueError("URL is required")
        return self._request


# --- Abstract Factory (simplified) ---


class UITheme(ABC):
    """Abstract factory for UI components."""

    @abstractmethod
    def create_button(self, text: str) -> str: ...

    @abstractmethod
    def create_input(self, placeholder: str) -> str: ...


class LightTheme(UITheme):
    def create_button(self, text: str) -> str:
        return f"[Light Button: {text}]"

    def create_input(self, placeholder: str) -> str:
        return f"[Light Input: {placeholder}]"


class DarkTheme(UITheme):
    def create_button(self, text: str) -> str:
        return f"[Dark Button: {text}]"

    def create_input(self, placeholder: str) -> str:
        return f"[Dark Input: {placeholder}]"


def get_theme(name: str) -> UITheme:
    themes: dict[str, type[UITheme]] = {"light": LightTheme, "dark": DarkTheme}
    klass = themes.get(name)
    if klass is None:
        raise ValueError(f"Unknown theme: {name}")
    return klass()


if __name__ == "__main__":
    print("=== Singleton ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"  Same instance? {db1 is db2}")
    db1.connect("postgres://localhost/mydb")
    print(f"  Active connections: {db2.active_connections()}")

    print("\n=== Factory ===")
    for channel, target in [
        ("email", "bob@test.com"),
        ("sms", "+1234567890"),
        ("push", "device-42"),
    ]:
        notif = NotificationFactory.create(channel, target)
        print(f"  {notif.send('Hello!')}")

    print("\n=== Builder ===")
    request = (
        RequestBuilder()
        .method("POST")
        .url("https://api.example.com/users")
        .header("Content-Type", "application/json")
        .header("Authorization", "Bearer token123")
        .body('{"name": "Alice"}')
        .timeout(10)
        .build()
    )
    print(f"  {request}")

    print("\n=== Abstract Factory ===")
    for theme_name in ["light", "dark"]:
        theme = get_theme(theme_name)
        print(
            f"  {theme.create_button('Submit')} {theme.create_input('Enter name...')}"
        )
