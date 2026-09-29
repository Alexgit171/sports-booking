"""Операции со спортивными площадками для практической работы № 2."""

from collections.abc import Iterable, Iterator
from typing import Any


Ground = dict[str, Any]


def next_ground_id(grounds: Iterable[Ground]) -> int:
    """Вернуть следующий свободный целочисленный идентификатор площадки."""
    return max((int(ground["id"]) for ground in grounds), default=0) + 1


def add_ground(
    grounds: list[Ground],
    name: str,
    sport: str,
    hourly_rate: float,
    open_hour: int,
    close_hour: int,
) -> Ground:
    """Проверить данные, добавить площадку и вернуть созданную запись."""
    clean_name = name.strip()
    clean_sport = sport.strip()
    if not clean_name or not clean_sport:
        raise ValueError("Название площадки и вид спорта не должны быть пустыми.")
    if hourly_rate <= 0:
        raise ValueError("Стоимость часа должна быть больше нуля.")
    if not 0 <= open_hour < close_hour <= 24:
        raise ValueError("Часы работы должны входить в диапазон от 0 до 24.")

    ground: Ground = {
        "id": next_ground_id(grounds),
        "name": clean_name,
        "sport": clean_sport,
        "hourly_rate": float(hourly_rate),
        "open_hour": int(open_hour),
        "close_hour": int(close_hour),
    }
    grounds.append(ground)
    return ground


def find_ground(grounds: Iterable[Ground], ground_id: int) -> Ground | None:
    """Найти площадку по идентификатору или вернуть ``None``."""
    return next(
        (ground for ground in grounds if int(ground["id"]) == ground_id),
        None,
    )


def search_grounds(grounds: Iterable[Ground], query: str) -> list[Ground]:
    """Найти площадки по части названия или вида спорта без учёта регистра."""
    normalized = query.strip().casefold()
    if not normalized:
        return list(grounds)
    return [
        ground
        for ground in grounds
        if normalized in str(ground["name"]).casefold()
        or normalized in str(ground["sport"]).casefold()
    ]


def filter_grounds(
    grounds: Iterable[Ground],
    sport: str | None = None,
    max_rate: float | None = None,
) -> Iterator[Ground]:
    """Сгенерировать площадки, подходящие по виду спорта и максимальной цене."""
    normalized_sport = sport.strip().casefold() if sport else None
    for ground in grounds:
        same_sport = (
            normalized_sport is None
            or str(ground["sport"]).casefold() == normalized_sport
        )
        affordable = max_rate is None or float(ground["hourly_rate"]) <= max_rate
        if same_sport and affordable:
            yield ground


def sort_grounds(
    grounds: Iterable[Ground],
    key: str = "name",
    reverse: bool = False,
) -> list[Ground]:
    """Вернуть новый список площадок, отсортированный по названию или цене."""
    key_functions = {
        "name": lambda ground: str(ground["name"]).casefold(),
        "rate": lambda ground: float(ground["hourly_rate"]),
    }
    if key not in key_functions:
        raise ValueError("Доступная сортировка: name или rate.")
    return sorted(grounds, key=key_functions[key], reverse=reverse)


def format_ground(ground: Ground) -> str:
    """Подготовить одну площадку для вывода в консоль."""
    return (
        f'#{ground["id"]} {ground["name"]} — {ground["sport"]}; '
        f'{int(ground["open_hour"]):02d}:00–{int(ground["close_hour"]):02d}:00; '
        f'{float(ground["hourly_rate"]):.2f} руб./ч'
    )
