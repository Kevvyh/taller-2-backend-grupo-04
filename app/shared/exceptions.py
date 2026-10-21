import logging
from typing import Final

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.api_response import error_response
from app.shared.types import FieldErrors

logger = logging.getLogger(__name__)


def conflict(errors: FieldErrors) -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={"message": "Conflicto con datos existentes", "errors": errors},
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: FieldErrors = {}

    for err in exc.errors():
        field = str(err["loc"][-1]) if err["loc"] else "body"
        err_type = err["type"]

        if err_type == "extra_forbidden":
            continue

        if err_type == "missing":
            message = _missing_field_message(request.url.path, field)
        else:
            message = err["msg"]
            if message.startswith("Value error, "):
                message = message[len("Value error, ") :]

        if field in errors:
            errors[field]["message"] += f", {message}"
        else:
            errors[field] = {"message": message}

    return JSONResponse(
        status_code=400,
        content=error_response(400, "Error de validación", errors=errors),
    )


STUDENT_MISSING_MESSAGES: Final[dict[str, str]] = {
    "name": (
        "El nombre debe ser un texto, El nombre no puede estar vacío, "
        "El nombre debe tener entre 3 y 100 caracteres, No se permiten etiquetas HTML"
    ),
    "username": (
        "El nombre de usuario debe ser un texto, "
        "El nombre de usuario no puede estar vacío, "
        "El nombre de usuario debe tener entre 3 y 30 caracteres, "
        "El nombre de usuario solo puede contener minúsculas, números y guiones bajos"
    ),
    "email": "El correo electrónico no es válido, El correo electrónico no puede estar vacío",
    "age": (
        "La edad debe ser un número entero, La edad debe ser al menos 18, "
        "La edad debe ser como máximo 99"
    ),
}

PET_MISSING_MESSAGES: Final[dict[str, str]] = {
    "name": (
        "El nombre debe ser un texto, El nombre no puede estar vacío, "
        "El nombre debe tener entre 1 y 50 caracteres, No se permiten etiquetas HTML"
    ),
    "species": (
        "La especie debe ser un texto, La especie no puede estar vacía, "
        "La especie debe tener entre 1 y 50 caracteres, No se permiten etiquetas HTML"
    ),
    "age": (
        "La edad debe ser un número entero, La edad debe ser al menos 0, "
        "La edad debe ser como máximo 100"
    ),
}


def _missing_field_message(path: str, field: str) -> str:
    table = PET_MISSING_MESSAGES if "/pets" in path else STUDENT_MISSING_MESSAGES
    return table.get(field, "El campo es obligatorio")


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    detail = exc.detail

    if isinstance(detail, dict) and "errors" in detail:
        message = detail.get("message", "Conflicto con datos existentes")
        body = error_response(exc.status_code, message, errors=detail["errors"])
    else:
        message = detail if isinstance(detail, str) else str(detail)
        body = error_response(exc.status_code, message, error=message)

    return JSONResponse(status_code=exc.status_code, content=body)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content=error_response(
            500, "Error interno del servidor", error="Error interno del servidor"
        ),
    )
