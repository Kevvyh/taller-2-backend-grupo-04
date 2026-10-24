from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.shared.database import Base
from app.shared.in_memory_store import InMemoryStore
from app.students.students_schemas import Student


def _utc_now() -> datetime:
    return datetime.now(UTC)


class StudentModel(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now)
    updated_at = Column(
        DateTime, nullable=False, default=_utc_now, onupdate=_utc_now
    )

    pets = relationship(
        "PetModel",
        back_populates="student",
        cascade="all, delete-orphan",
    )


def _to_schema(model: StudentModel) -> Student:
    return Student(
        id=model.id,
        name=model.name,
        username=model.username,
        email=model.email,
        age=model.age,
        createdAt=model.created_at,
        updatedAt=model.updated_at,
    )

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
