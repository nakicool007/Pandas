from __future__ import annotations
from .library import Library
from .errors import LibraryError


def main() -> None:
    lib = Library()

    MENU = """
--- Student Library System ---
1. Add Student
2. List Students
3. View Student
4. Update Student
5. Delete Student
6. Search
7. Exit
"""

    while True:
        print(MENU)
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                name = input("Name: ")
                book = input("Book: ")
                genre = input("Genre: ")
                lib.add_student(name, book, genre)
                print("✅ Added.")
            elif choice == "2":
                print(lib)
            elif choice == "3":
                name = input("Name to view: ")
                print(lib.get_student(name))
            elif choice == "4":
                name = input("Current name: ")
                new_name = input("New name (blank to keep): ").strip() or None
                book = input("New book (blank to keep): ").strip() or None
                genre = input("New genre (blank to keep): ").strip() or None
                updated = lib.update_student(name, book=book, genre=genre, new_name=new_name)
                print("✅ Updated:", updated)
            elif choice == "5":
                name = input("Name to delete: ")
                lib.delete_student(name)
                print("🗑️ Deleted.")
            elif choice == "6":
                q = input("Name contains (blank to skip): ").strip() or None
                genre = input("Genre equals (blank to skip): ").strip() or None
                book = input("Book equals (blank to skip): ").strip() or None
                results = lib.search(name_contains=q, genre=genre, book=book)
                print("\n".join(str(s) for s in results) or "No matches.")
            elif choice == "7":
                print("Bye!")
                break
            else:
                print("Invalid choice.")
        except LibraryError as e:
            print(f"⚠️ {e}")


if __name__ == "__main__":
    main()
