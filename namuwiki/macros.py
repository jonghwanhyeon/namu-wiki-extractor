import re
from datetime import date
from typing import Callable, Optional


def _parse_date(date_text: str) -> Optional[date]:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_text.strip())
    if match is None:
        return None

    return date(
        year=int(match.group(1)), month=int(match.group(2)), day=int(match.group(3))
    )


def default(parameter: str) -> str:
    return " "


def age(parameter: str) -> str:
    date = _parse_date(parameter)
    if date is None:
        return " "

    today = date.today()

    value = today.year - date.year
    if (today.month, today.day) < (date.month, date.day):
        value -= 1

    return str(value)


def dday(parameter: str) -> str:
    date = _parse_date(parameter)
    if date is None:
        return " "

    today = date.today()

    value = today - date
    return "{:+}".format(value.days)


def ruby(parameter: str) -> str:
    match = re.search(r'^([^,]*)', parameter)
    if match is None:
        return " "

    return match.group(1)


def resolve(name: str) -> Callable[[Optional[str]], str]:
    environment = globals()
    return environment[name] if name in environment else default
