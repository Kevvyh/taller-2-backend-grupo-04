from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.pets.pets_schemas import Pet
from app.shared.database import Base, SessionLocal
from app.students.students_repository import StudentModel


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    name = Column(String, nullable=False)
    specie = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    student = relationship("StudentModel", back_populates="pets")


def _to_schema(model: PetModel) -> Pet:
    return Pet(
        id=model.id,
        studentId=model.student_id,
        name=model.name,
        species=model.specie,
        age=model.age,
        createdAt=model.created_at,
        updatedAt=model.updated_at,
    )


class PetsRepository:
    def find_all(self) -> list[Pet]:
        with SessionLocal() as session:
            models = session.query(PetModel).all()
            return [_to_schema(m) for m in models]

    def find_all_by_student(self, student_id: str) -> list[Pet]:
        with SessionLocal() as session:
            models = (
                session.query(PetModel)
                .filter(PetModel.student_id == student_id)
                .all()
            )
            return [_to_schema(m) for m in models]

    def find_by_id(self, pet_id: str) -> Pet | None:
        with SessionLocal() as session:
            model = session.get(PetModel, pet_id)
            return _to_schema(model) if model else None

    def find_by_student_and_name(self, student_id: str, name: str) -> Pet | None:
        with SessionLocal() as session:
            model = (
                session.query(PetModel)
                .filter(PetModel.student_id == student_id, PetModel.name == name)
                .first()
            )
            return _to_schema(model) if model else None

    def save(self, pet: Pet) -> Pet:
        with SessionLocal() as session:
            try:
                db_pet = session.get(PetModel, pet.id)
                if db_pet is None:
                    db_pet = PetModel(
                        id=pet.id,
                        student_id=pet.studentId,
                        name=pet.name,
                        specie=pet.species,
                        age=pet.age,
                        created_at=pet.createdAt,
                        updated_at=pet.updatedAt,
                    )
                    session.add(db_pet)
                else:
                    db_pet.name = pet.name
                    db_pet.specie = pet.species
                    db_pet.age = pet.age
                    db_pet.updated_at = pet.updatedAt
                session.commit()
                session.refresh(db_pet)
                return _to_schema(db_pet)
            except Exception as e:
                session.rollback()
                raise e
            
    def delete(self, pet_id: str) -> None:
        with SessionLocal() as session:
            try:
                db_pet = session.get(PetModel, pet_id)
                if db_pet:
                    session.delete(db_pet)
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e
            
    def delete_by_student(self, student_id: str) -> None:
        with SessionLocal() as session:
            try:
                session.query(PetModel).filter(PetModel.student_id == student_id).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                raise e


pets_repository = PetsRepository()