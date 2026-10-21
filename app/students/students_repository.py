from app.shared.in_memory_store import InMemoryStore
from app.students.students_schemas import Student


class StudentsRepository:
    def __init__(self) -> None:
        self._store: InMemoryStore[Student] = InMemoryStore()

    def find_all(self) -> list[Student]:
        return self._store.find_all()

    def find_by_id(self, student_id: str) -> Student | None:
        return self._store.get(student_id)

    def find_by_email(self, email: str) -> Student | None:
        matches = self._store.find_by(lambda student: student.email == email)
        return matches[0] if matches else None

    def find_by_username(self, username: str) -> Student | None:
        matches = self._store.find_by(lambda student: student.username == username)
        return matches[0] if matches else None

    def save(self, student: Student) -> Student:
        self._store.set(student)
        return student

    def delete(self, student_id: str) -> None:
        self._store.delete(student_id)
