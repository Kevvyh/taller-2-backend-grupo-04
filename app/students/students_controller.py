from fastapi import APIRouter

from app.pets.pets_service import pets_service
from app.students.students_schemas import (
    CreateStudentDto,
    Student,
    StudentList,
    UpdateStudentDto,
)
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def find_all() -> StudentList:
    return students_service.find_all()


@router.get("/{studentId}")
def find_by_id(studentId: str) -> Student:
    return students_service.find_by_id(studentId)


@router.post("", status_code=201)
def create(body: CreateStudentDto) -> Student:
    return students_service.create(body)


@router.patch("/{studentId}")
def update(studentId: str, body: UpdateStudentDto) -> Student:
    return students_service.update(studentId, body)


@router.delete("/{studentId}")
def delete(studentId: str) -> Student:
    deleted = students_service.delete(studentId)
    pets_service.delete_all_for_student(studentId)

    return deleted
