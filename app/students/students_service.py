from uuid import uuid4

from fastapi import HTTPException, status

from app.pets.pets_repository import PetsRepository, pets_repository
from app.pets.pets_schemas import Pet
from app.shared.datetimes import utc_now
from app.shared.exceptions import conflict
from app.shared.types import FieldErrors
from app.students.students_repository import StudentsRepository
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)


class StudentsService:
    def __init__(self, repository: StudentsRepository, pets: PetsRepository) -> None:
        self.repository = repository
        self.pets_repository = pets

    def find_all(self) -> StudentList:
        students = sorted(
            self.repository.find_all(), key=lambda s: s.createdAt, reverse=True
        )

        return StudentList(total=len(students), items=students)

    def find_by_id(self, student_id: str) -> Student:
        student = self.repository.find_by_id(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        return student

    def create(self, data: CreateStudentDto) -> Student:
        self.assert_no_conflicts(data)

        now = utc_now()
        student = Student(
            id=str(uuid4()),
            name=data.name,
            username=data.username,
            email=data.email,
            age=data.age,
            createdAt=now,
            updatedAt=now,
        )

        self.repository.save(student)

        # En SQL/ORM, insertar el estudiante y sus mascotas debe ir dentro de una
        # transacción: si una mascota falla, el estudiante no debe quedar creado.
        for pet_data in data.pets:
            existing = self.pets_repository.find_by_student_and_name(
                student.id, pet_data.name
            )

            if existing is not None:
                raise conflict(
                    {"name": {"message": "Ya tienes una mascota con ese nombre"}}
                )

            pet_now = utc_now()
            pet = Pet(
                id=str(uuid4()),
                studentId=student.id,
                name=pet_data.name,
                species=pet_data.species,
                age=pet_data.age,
                createdAt=pet_now,
                updatedAt=pet_now,
            )

            self.pets_repository.save(pet)

        return student

    def update(self, student_id: str, data: UpdateStudentDto) -> Student:
        existing = self.find_by_id(student_id)
        self.assert_no_conflicts(data, except_id=student_id)

        updated = existing.model_copy(
            update={
                **data.model_dump(exclude_none=True),
                "updatedAt": utc_now(),
            }
        )

        return self.repository.save(updated)

    def delete(self, student_id: str) -> Student:
        existing = self.find_by_id(student_id)
        self.repository.delete(student_id)

        return existing

    def assert_no_conflicts(
        self,
        data: CreateStudentDto | UpdateStudentDto,
        except_id: str | None = None,
    ) -> None:
        errors: FieldErrors = {}

        if data.email:
            existing = self.repository.find_by_email(data.email)
            if existing and existing.id != except_id:
                errors["email"] = {"message": "El correo electrónico ya está en uso"}

        if data.username:
            existing = self.repository.find_by_username(data.username)
            if existing and existing.id != except_id:
                errors["username"] = {"message": "El nombre de usuario ya está en uso"}

        if errors:
            raise conflict(errors)


students_repository = StudentsRepository()
students_service = StudentsService(students_repository, pets_repository)
