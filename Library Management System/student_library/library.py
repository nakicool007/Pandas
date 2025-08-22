from __future__ import annotations
import json
from pathlib import Path
from typing import List, Iterable, Optional

from .student import Student
from .errors import DuplicateStudentError, NotFoundError


class Library:
    """
    Manages students and persistence to a JSON file.
    """

    def __init__(self, storage_path: str | Path = "data/students.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._students: List[Student] = []
        self._load()

    # ---------- Persistence ----------
    def _load(self) -> None:
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self._students = [Student.from_dict(d) for d in data]
        else:
            self._students = []

    def _save(self) -> None:
        payload = [s.to_dict() for s in self._students]
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # ---------- CRUD ----------
    def add_student(self, name: str, book: str, genre: str) -> Student:
        name = name.strip()
        if any(s.name.lower() == name.lower() for s in self._students):
            raise DuplicateStudentError(f"Student '{name}' already exists.")
        student = Student(name=name, book=book.strip(), genre=genre.strip())
        self._students.append(student)
        self._save()
        return student

    def list_students(self) -> List[Student]:
        return list(self._students)

    def get_student(self, name: str) -> Student:
        for s in self._students:
            if s.name.lower() == name.strip().lower():
                return s
        raise NotFoundError(f"Student '{name}' not found.")

    def update_student(
        self,
        name: str,
        book: Optional[str] = None,
        genre: Optional[str] = None,
        new_name: Optional[str] = None,
    ) -> Student:
        idx = None
        for i, s in enumerate(self._students):
            if s.name.lower() == name.strip().lower():
                idx = i
                break
        if idx is None:
            raise NotFoundError(f"Student '{name}' not found.")

        current = self._students[idx]
        next_name = new_name.strip() if new_name else current.name
        # Prevent rename collision
        if new_name and any(
            s.name.lower() == next_name.lower() and s is not current for s in self._students
        ):
            raise DuplicateStudentError(f"Student '{next_name}' already exists.")

        updated = Student(
            name=next_name,
            book=(book.strip() if book is not None else current.book),
            genre=(genre.strip() if genre is not None else current.genre),
        )
        self._students[idx] = updated
        self._save()
        return updated

    def delete_student(self, name: str) -> None:
        before = len(self._students)
        self._students = [s for s in self._students if s.name.lower() != name.strip().lower()]
        if len(self._students) == before:
            raise NotFoundError(f"Student '{name}' not found.")
        self._save()

    # ---------- Queries ----------
    def search(
        self, *, name_contains: str | None = None, genre: str | None = None, book: str | None = None
    ) -> Iterable[Student]:
        def match(s: Student) -> bool:
            return all([
                (name_contains.lower() in s.name.lower()) if name_contains else True,
                (s.genre.lower() == genre.lower()) if genre else True,
                (s.book.lower() == book.lower()) if book else True,
            ])
        return [s for s in self._students if match(s)]

    def __str__(self) -> str:
        if not self._students:
            return "No students found."
        lines = [f"{i+1}. {str(s)}" for i, s in enumerate(self._students)]
        return "\n".join(lines)
