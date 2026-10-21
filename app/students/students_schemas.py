from typing import Final

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.pets.pets_schemas import CreatePetDto
from app.shared.datetimes import ApiDatetime
from app.shared.validation import validate_email, validate_int, validate_text

NO_HTML_PATTERN: Final[str] = r"^[^<>]*$"
USERNAME_PATTERN: Final[str] = r"^[a-z0-9_]+$"

STUDENT_NAME_MESSAGES: Final[dict[str, str]] = {
    "type": "El nombre debe ser un texto",
    "empty": "El nombre no puede estar vacío",
    "length": "El nombre debe tener entre 3 y 100 caracteres",
    "pattern": "No se permiten etiquetas HTML",
}
USERNAME_MESSAGES: Final[dict[str, str]] = {
    "type": "El nombre de usuario debe ser un texto",
    "empty": "El nombre de usuario no puede estar vacío",
    "length": "El nombre de usuario debe tener entre 3 y 30 caracteres",
    "pattern": "El nombre de usuario solo puede contener minúsculas, números y guiones bajos",
}
EMAIL_MESSAGES: Final[dict[str, str]] = {
    "invalid": "El correo electrónico no es válido",
    "empty": "El correo electrónico no puede estar vacío",
}
STUDENT_AGE_MESSAGES: Final[dict[str, str]] = {
    "type": "La edad debe ser un número entero",
    "min": "La edad debe ser al menos 18",
    "max": "La edad debe ser como máximo 99",
}


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    username: str
    email: EmailStr
    age: int
    createdAt: ApiDatetime
    updatedAt: ApiDatetime


class StudentList(BaseModel):
    total: int
    items: list[Student]


class CreateStudentDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=100, pattern=NO_HTML_PATTERN)
    username: str = Field(min_length=3, max_length=30, pattern=USERNAME_PATTERN)
    email: EmailStr
    age: int = Field(ge=18, le=99)
    pets: list[CreatePetDto] = Field(default_factory=list)

    @field_validator("name", mode="before")
    @classmethod
    def _validate_name(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=STUDENT_NAME_MESSAGES["type"],
                empty_message=STUDENT_NAME_MESSAGES["empty"],
                length_message=STUDENT_NAME_MESSAGES["length"],
                pattern_message=STUDENT_NAME_MESSAGES["pattern"],
                min_length=3,
                max_length=100,
                pattern=NO_HTML_PATTERN,
                check_empty=True,
                allow_none=False,
            )
        )
        return v

    @field_validator("username", mode="before")
    @classmethod
    def _validate_username(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=USERNAME_MESSAGES["type"],
                empty_message=USERNAME_MESSAGES["empty"],
                length_message=USERNAME_MESSAGES["length"],
                pattern_message=USERNAME_MESSAGES["pattern"],
                min_length=3,
                max_length=30,
                pattern=USERNAME_PATTERN,
                check_empty=True,
                allow_none=False,
            )
        )
        return v

    @field_validator("email", mode="before")
    @classmethod
    def _validate_email(cls, v: object) -> object:
        _raise_validation(
            validate_email(
                v,
                invalid_message=EMAIL_MESSAGES["invalid"],
                empty_message=EMAIL_MESSAGES["empty"],
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
                type_message=STUDENT_AGE_MESSAGES["type"],
                min_message=STUDENT_AGE_MESSAGES["min"],
                max_message=STUDENT_AGE_MESSAGES["max"],
                min_value=18,
                max_value=99,
                allow_none=False,
            )
        )
        return v


class UpdateStudentDto(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None, min_length=3, max_length=100, pattern=NO_HTML_PATTERN
    )
    username: str | None = Field(
        default=None, min_length=3, max_length=30, pattern=USERNAME_PATTERN
    )
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=99)

    @field_validator("name", mode="before")
    @classmethod
    def _validate_name(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=STUDENT_NAME_MESSAGES["type"],
                empty_message=STUDENT_NAME_MESSAGES["empty"],
                length_message=STUDENT_NAME_MESSAGES["length"],
                pattern_message=STUDENT_NAME_MESSAGES["pattern"],
                min_length=3,
                max_length=100,
                pattern=NO_HTML_PATTERN,
                check_empty=False,
                allow_none=True,
            )
        )
        return v

    @field_validator("username", mode="before")
    @classmethod
    def _validate_username(cls, v: object) -> object:
        _raise_validation(
            validate_text(
                v,
                type_message=USERNAME_MESSAGES["type"],
                empty_message=USERNAME_MESSAGES["empty"],
                length_message=USERNAME_MESSAGES["length"],
                pattern_message=USERNAME_MESSAGES["pattern"],
                min_length=3,
                max_length=30,
                pattern=USERNAME_PATTERN,
                check_empty=False,
                allow_none=True,
            )
        )
        return v

    @field_validator("email", mode="before")
    @classmethod
    def _validate_email(cls, v: object) -> object:
        _raise_validation(
            validate_email(
                v,
                invalid_message=EMAIL_MESSAGES["invalid"],
                empty_message=EMAIL_MESSAGES["empty"],
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
                type_message=STUDENT_AGE_MESSAGES["type"],
                min_message=STUDENT_AGE_MESSAGES["min"],
                max_message=STUDENT_AGE_MESSAGES["max"],
                min_value=18,
                max_value=99,
                allow_none=True,
            )
        )
        return v


def _raise_validation(messages: list[str]) -> None:
    if messages:
        raise ValueError(", ".join(messages))
