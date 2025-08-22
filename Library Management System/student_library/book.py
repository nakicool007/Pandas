from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    title: str
    genre: str

    def __str__(self) -> str:
        return f"{self.title} ({self.genre})"
