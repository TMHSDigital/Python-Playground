"""Dataclasses: structured data with minimal boilerplate.

Dataclasses (Python 3.7+) auto-generate __init__, __repr__, __eq__,
and more. This module covers basic through advanced usage.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import ClassVar


# --- Basic Dataclass ---


@dataclass
class Coordinate:
    """A 2D coordinate with comparison support."""

    x: float
    y: float

    def distance_to(self, other: Coordinate) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# --- Default Values and Field Factories ---


@dataclass
class Config:
    """Application configuration with defaults and field factories."""

    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def base_url(self) -> str:
        scheme = "http" if self.debug else "https"
        return f"{scheme}://{self.host}:{self.port}"


# --- Frozen (Immutable) Dataclass ---


@dataclass(frozen=True)
class Color:
    """An immutable RGB color."""

    r: int
    g: int
    b: int

    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @classmethod
    def from_hex(cls, hex_str: str) -> Color:
        hex_str = hex_str.lstrip("#")
        return cls(
            r=int(hex_str[0:2], 16),
            g=int(hex_str[2:4], 16),
            b=int(hex_str[4:6], 16),
        )


# --- Ordered Dataclass ---


@dataclass(order=True)
class Version:
    """Semantic version with natural ordering."""

    sort_index: tuple = field(init=False, repr=False)
    major: int
    minor: int
    patch: int

    def __post_init__(self):
        self.sort_index = (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


# --- Inheritance ---


class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class Task:
    """A basic task with a title and completion status."""

    title: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)

    def complete(self) -> Task:
        self.completed = True
        return self


@dataclass
class TimedTask(Task):
    """A task with an estimated duration in minutes."""

    estimated_minutes: int = 30

    def is_quick(self) -> bool:
        return self.estimated_minutes <= 15


# --- ClassVar and Serialization ---


@dataclass
class User:
    """A user with serialization support."""

    _next_id: ClassVar[int] = 1

    name: str
    email: str
    id: int = field(init=False)
    active: bool = True

    def __post_init__(self):
        self.id = User._next_id
        User._next_id += 1

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> User:
        user = cls(name=data["name"], email=data["email"])
        user.active = data.get("active", True)
        return user


# --- Slots (Python 3.10+) ---


@dataclass(slots=True)
class Vector3D:
    """A 3D vector using __slots__ for memory efficiency."""

    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def dot(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3D) -> Vector3D:
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


if __name__ == "__main__":
    print("=== Coordinate ===")
    a, b = Coordinate(0, 0), Coordinate(3, 4)
    print(f"  {a} -> {b}: distance={a.distance_to(b)}")

    print("\n=== Config ===")
    cfg = Config(host="api.example.com", port=443, tags=["prod"])
    print(f"  {cfg}")
    print(f"  URL: {cfg.base_url()}")

    print("\n=== Color (frozen) ===")
    red = Color(255, 0, 0)
    blue = Color.from_hex("#0000ff")
    print(f"  {red} -> {red.hex()}")
    print(f"  {blue} -> {blue.hex()}")

    print("\n=== Version (ordered) ===")
    versions = [Version(2, 0, 0), Version(1, 9, 1), Version(1, 10, 0)]
    print(f"  sorted: {[str(v) for v in sorted(versions)]}")

    print("\n=== Task ===")
    task = TimedTask("Write docs", priority=Priority.HIGH, estimated_minutes=10)
    print(f"  {task}")
    print(f"  Quick? {task.is_quick()}")

    print("\n=== User (auto-id) ===")
    u1 = User("Alice", "alice@example.com")
    u2 = User("Bob", "bob@example.com")
    print(f"  {u1}")
    print(f"  {u2}")
    print(f"  JSON: {u1.to_json()}")

    print("\n=== Vector3D (slots) ===")
    v1 = Vector3D(1, 0, 0)
    v2 = Vector3D(0, 1, 0)
    print(f"  {v1} x {v2} = {v1.cross(v2)}")
    print(f"  |{v1}| = {v1.magnitude()}")
