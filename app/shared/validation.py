import re

from email_validator import EmailNotValidError
from email_validator import validate_email as check_email_address


def _is_empty(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value == ""
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, dict):
        return len(value) == 0
    return False


def _is_js_integer(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and float(value).is_integer()
    )


def validate_text(
    value: object,
    *,
    type_message: str,
    empty_message: str,
    length_message: str,
    pattern_message: str,
    min_length: int,
    max_length: int,
    pattern: str,
    check_empty: bool,
    allow_none: bool,
) -> list[str]:
    if allow_none and value is None:
        return []

    errors: list[str] = []
    is_str = isinstance(value, str)

    if not is_str:
        errors.append(type_message)

    if check_empty and _is_empty(value):
        errors.append(empty_message)

    if not (is_str and min_length <= len(value) <= max_length):
        errors.append(length_message)

    if not (is_str and re.match(pattern, value)):
        errors.append(pattern_message)

    return errors


def validate_email(
    value: object,
    *,
    invalid_message: str,
    empty_message: str,
    check_empty: bool,
    allow_none: bool,
) -> list[str]:
    if allow_none and value is None:
        return []

    errors: list[str] = []
    is_valid = isinstance(value, str) and _is_email(value)

    if not is_valid:
        errors.append(invalid_message)

    if check_empty and _is_empty(value):
        errors.append(empty_message)

    return errors


def _is_email(value: str) -> bool:
    try:
        check_email_address(value, check_deliverability=False)
    except EmailNotValidError:
        return False
    return True


def _js_gte(value: object, bound: int) -> bool:
    if isinstance(value, bool):
        return (1 if value else 0) >= bound
    if isinstance(value, (int, float)):
        return value >= bound
    if value is None:
        return 0 >= bound
    return False


def _js_lte(value: object, bound: int) -> bool:
    if isinstance(value, bool):
        return (1 if value else 0) <= bound
    if isinstance(value, (int, float)):
        return value <= bound
    if value is None:
        return 0 <= bound
    return False


def validate_int(
    value: object,
    *,
    type_message: str,
    min_message: str,
    max_message: str,
    min_value: int,
    max_value: int,
    allow_none: bool,
) -> list[str]:
    if allow_none and value is None:
        return []

    errors: list[str] = []

    if not _is_js_integer(value):
        errors.append(type_message)

    if not _js_gte(value, min_value):
        errors.append(min_message)

    if not _js_lte(value, max_value):
        errors.append(max_message)

    return errors
