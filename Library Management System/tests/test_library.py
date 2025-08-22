import json
from pathlib import Path
import pytest

from student_library.library import Library
from student_library.errors import DuplicateStudentError, NotFoundError


def test_add_and_list(tmp_path: Path):
    lib = Library(storage_path=tmp_path / "students.json")
    lib.add_student("Alice", "Boogie", "Dance")
    lib.add_student("Bob", "Dune", "Sci-Fi")

    names = [s.name for s in lib.list_students()]
    assert names == ["Alice", "Bob"]

    # persisted
    raw = json.loads((tmp_path / "students.json").read_text(encoding="utf-8"))
    assert raw[0]["name"] == "Alice"


def test_duplicate_student(tmp_path: Path):
    lib = Library(storage_path=tmp_path / "students.json")
    lib.add_student("Alice", "Boogie", "Dance")
    with pytest.raises(DuplicateStudentError):
        lib.add_student("alice", "Other", "Other")  # case-insensitive dup


def test_get_update_delete(tmp_path: Path):
    lib = Library(storage_path=tmp_path / "students.json")
    lib.add_student("Alice", "Boogie", "Dance")
    s = lib.get_student("Alice")
    assert s.book == "Boogie"

    updated = lib.update_student("Alice", book="Boogie 2", genre="Dance", new_name="Alicia")
    assert updated.name == "Alicia"
    assert lib.get_student("Alicia").book == "Boogie 2"

    lib.delete_student("Alicia")
    with pytest.raises(NotFoundError):
        lib.get_student("Alicia")


def test_search(tmp_path: Path):
    lib = Library(storage_path=tmp_path / "students.json")
    lib.add_student("Alice", "Boogie", "Dance")
    lib.add_student("Alina", "Boogie", "Dance")
    lib.add_student("Bob", "Dune", "Sci-Fi")

    results = list(lib.search(name_contains="ali"))
    assert [s.name for s in results] == ["Alice", "Alina"]

    results = list(lib.search(genre="Sci-Fi"))
    assert [s.name for s in results] == ["Bob"]
