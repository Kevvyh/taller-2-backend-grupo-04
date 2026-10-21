import json
from collections.abc import Awaitable, Callable
from typing import Final

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from app.shared.datetimes import now_iso
from app.shared.types import Envelope, FieldErrors

MESSAGE_BY_METHOD: Final[dict[str, str]] = {
    "GET": "Operación exitosa",
    "POST": "Recurso creado",
    "PATCH": "Recurso actualizado",
    "DELETE": "Recurso eliminado",
}


def success_response(code: int, message: str, data: object) -> Envelope:
    return {
        "code": code,
        "success": True,
        "message": message,
        "timestamp": now_iso(),
        "data": data,
    }


def error_response(
    code: int,
    message: str,
    *,
    error: str | None = None,
    errors: FieldErrors | None = None,
) -> Envelope:
    body: Envelope = {
        "code": code,
        "success": False,
        "message": message,
        "timestamp": now_iso(),
        "data": None,
    }

    if errors is not None:
        body["errors"] = errors
    elif error is not None:
        body["error"] = error

    return body


async def envelope_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    response: Response = await call_next(request)

    if not request.url.path.startswith("/api") or not 200 <= response.status_code < 400:
        return response

    body_bytes = getattr(response, "body", None)
    if body_bytes is None:
        body_bytes = b"".join([chunk async for chunk in response.body_iterator])

    data = json.loads(body_bytes)
    message = MESSAGE_BY_METHOD.get(request.method, "OK")
    body = success_response(response.status_code, message, data)

    return JSONResponse(status_code=response.status_code, content=body)
