from datetime import UTC, datetime
from typing import Annotated

from pydantic import PlainSerializer


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_ms(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{dt.microsecond // 1000:03d}Z"


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


type ApiDatetime = Annotated[datetime, PlainSerializer(iso_ms, return_type=str)]
