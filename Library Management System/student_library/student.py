from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class Student:
    """
    Represents a student with a favorite book and genre.
    Use an immutable dataclass so instances are hashable and safe in collections.
    """
    name: str
    book: str
    genre: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Student":
        return cls(name=data["name"], book=data["book"], genre=data["genre"])

    def __str__(self) -> str:
        return f"{self.name} | Book: {self.book} | Genre: {self.genre}"
