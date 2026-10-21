from typing import Final

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.shared.datetimes import ApiDatetime
from app.shared.validation import validate_int, validate_text

NO_HTML_PATTERN: Final[str] = r"^[^<>]*$"

PET_NAME_MESSAGES: Final[dict[str, str]] = {
    "type": "El nombre debe ser un texto",
    "empty": "El nombre no puede estar vacío",
    "length": "El nombre debe tener entre 1 y 50 caracteres",
    "pattern": "No se permiten etiquetas HTML",
}
PET_SPECIES_MESSAGES: Final[dict[str, str]] = {
    "type": "La especie debe ser un texto",
    "empty": "La especie no puede estar vacía",
    "length": "La especie debe tener entre 1 y 50 caracteres",
    "pattern": "No se permiten etiquetas HTML",
}
PET_AGE_MESSAGES: Final[dict[str, str]] = {
    "type": "La edad debe ser un número entero",
    "min": "La edad debe ser al menos 0",
    "max": "La edad debe ser como máximo 100",
}


class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    studentId: str
    name: str
    species: str
    age: int | None = None
    createdAt: ApiDatetime
    updatedAt: ApiDatetime


class PetList(BaseModel):
    total: int
    items: list[Pet]


class CreatePetDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=50, pattern=NO_HTML_PATTERN)
    species: str = Field(min_length=1, max_length=50, pattern=NO_HTML_PATTERN)
    age: int | None = Field(default=None, ge=0, le=100)

    @field_validator("name", mode="before")
    @classmethod
    def _validate_name(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=PET_NAME_MESSAGES["type"],
                empty_message=PET_NAME_MESSAGES["empty"],
                length_message=PET_NAME_MESSAGES["length"],
                pattern_message=PET_NAME_MESSAGES["pattern"],
                min_length=1,
                max_length=50,
                pattern=NO_HTML_PATTERN,
                check_empty=True,
                allow_none=False,
            )
        )
        return v

    @field_validator("species", mode="before")
    @classmethod
    def _validate_species(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=PET_SPECIES_MESSAGES["type"],
                empty_message=PET_SPECIES_MESSAGES["empty"],
                length_message=PET_SPECIES_MESSAGES["length"],
                pattern_message=PET_SPECIES_MESSAGES["pattern"],
                min_length=1,
                max_length=50,
                pattern=NO_HTML_PATTERN,
                check_empty=True,
                allow_none=False,
            )
        )
        return v

    @field_validator("age", mode="before")
    @classmethod
    def _validate_age(cls, v: object) -> object:
        _raise_validation(
            validate_int(
                v,
                type_message=PET_AGE_MESSAGES["type"],
                min_message=PET_AGE_MESSAGES["min"],
                max_message=PET_AGE_MESSAGES["max"],
                min_value=0,
                max_value=100,
                allow_none=True,
            )
        )
        return v


class UpdatePetDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=NO_HTML_PATTERN
    )
    species: str | None = Field(
        default=None, min_length=1, max_length=50, pattern=NO_HTML_PATTERN
    )
    age: int | None = Field(default=None, ge=0, le=100)

    @field_validator("name", mode="before")
    @classmethod
    def _validate_name(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=PET_NAME_MESSAGES["type"],
                empty_message=PET_NAME_MESSAGES["empty"],
                length_message=PET_NAME_MESSAGES["length"],
                pattern_message=PET_NAME_MESSAGES["pattern"],
                min_length=1,
                max_length=50,
                pattern=NO_HTML_PATTERN,
                check_empty=False,
                allow_none=True,
            )
        )
        return v

    @field_validator("species", mode="before")
    @classmethod
    def _validate_species(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=PET_SPECIES_MESSAGES["type"],
                empty_message=PET_SPECIES_MESSAGES["empty"],
                length_message=PET_SPECIES_MESSAGES["length"],
                pattern_message=PET_SPECIES_MESSAGES["pattern"],
                min_length=1,
                max_length=50,
                pattern=NO_HTML_PATTERN,
                check_empty=False,
                allow_none=True,
            )
        )
        return v

    @field_validator("age", mode="before")
    @classmethod
    def _validate_age(cls, v: object) -> object:
        _raise_validation(
            validate_int(
                v,
                type_message=PET_AGE_MESSAGES["type"],
                min_message=PET_AGE_MESSAGES["min"],
                max_message=PET_AGE_MESSAGES["max"],
                min_value=0,
                max_value=100,
                allow_none=True,
            )
        )
        return v


def _raise_validation(messages: list[str]) -> None:
    if messages:
        raise ValueError(", ".join(messages))
