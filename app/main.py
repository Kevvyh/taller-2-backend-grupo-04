from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.pets.pets_controller import router as pets_router
from app.shared.api_response import envelope_middleware
from app.shared.exceptions import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.students.students_controller import router as students_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI CRUD Students & Pets",
        description=(
            "API de un CRUD en memoria para la entidad Student y sus mascotas (Pet)"
        ),
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    app.middleware("http")(envelope_middleware)

    app.include_router(students_router)
    app.include_router(pets_router)

    @app.api_route(
        "/api/{path:path}",
        methods=["GET", "POST", "PATCH", "DELETE", "PUT", "OPTIONS", "HEAD"],
    )
    def not_found_api(request: Request, path: str) -> None:
        raise HTTPException(
            status_code=404, detail=f"Cannot {request.method} /api/{path}"
        )

    app.mount("/", StaticFiles(directory="public", html=True), name="static")

    return app


app = create_app()
