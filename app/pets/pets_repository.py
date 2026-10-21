from app.pets.pets_schemas import Pet
from app.shared.in_memory_store import InMemoryStore


class PetsRepository:
    def __init__(self) -> None:
        self._store: InMemoryStore[Pet] = InMemoryStore()

    def find_all_by_student(self, student_id: str) -> list[Pet]:
        return self._store.find_by(lambda pet: pet.studentId == student_id)

    def find_by_id(self, pet_id: str) -> Pet | None:
        return self._store.get(pet_id)

    def find_by_student_and_name(self, student_id: str, name: str) -> Pet | None:
        matches = self._store.find_by(
            lambda pet: pet.studentId == student_id and pet.name == name
        )
        return matches[0] if matches else None

    def save(self, pet: Pet) -> Pet:
        self._store.set(pet)
        return pet

    def delete(self, pet_id: str) -> None:
        self._store.delete(pet_id)

    def delete_by_student(self, student_id: str) -> None:
        self._store.delete_by(lambda pet: pet.studentId == student_id)


pets_repository = PetsRepository()
