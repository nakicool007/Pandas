class LibraryError(Exception):
    """Base error for library operations."""


class DuplicateStudentError(LibraryError):
    """Raised when adding a student that already exists."""


class NotFoundError(LibraryError):
    """Raised when a requested entity is not found."""
