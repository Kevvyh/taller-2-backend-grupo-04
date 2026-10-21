from fastapi import APIRouter

from app.pets.pets_schemas import CreatePetDto, Pet, PetList, UpdatePetDto
from app.pets.pets_service import pets_service

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)


@router.get("")
def find_all(studentId: str) -> PetList:
    return pets_service.find_all_for_student(studentId)


@router.post("", status_code=201)
def create(studentId: str, body: CreatePetDto) -> Pet:
    return pets_service.create(studentId, body)


@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto) -> Pet:
    return pets_service.update(studentId, petId, body)


@router.delete("/{petId}")
def delete(studentId: str, petId: str) -> Pet:
    return pets_service.delete(studentId, petId)
