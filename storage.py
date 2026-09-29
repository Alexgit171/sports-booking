"""Чтение и сохранение данных проекта в формате JSON."""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_GROUNDS = [
    {
        "id": 1,
        "name": "СпортПарк, площадка для мини-футбола",
        "sport": "мини-футбол",
        "hourly_rate": 1500.0,
        "open_hour": 8,
        "close_hour": 22,
    },
    {
        "id": 2,
        "name": "Теннис Центр",
        "sport": "теннис",
        "hourly_rate": 1200.0,
        "open_hour": 9,
        "close_hour": 21,
    },
    {
        "id": 3,
        "name": "Баскет Холл",
        "sport": "баскетбол",
        "hourly_rate": 1800.0,
        "open_hour": 10,
        "close_hour": 23,
    },
]

DEFAULT_BOOKINGS = [
    {
        "id": 1,
        "user_name": "Учебная бронь ПР1",
        "ground_id": 1,
        "date": "2026-10-01",
        "start_hour": 18,
        "end_hour": 20,
        "duration": 2,
        "price": 3000.0,
        "status": "confirmed",
    }
]


def default_state() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Вернуть независимые копии демонстрационных данных."""
    return deepcopy(DEFAULT_GROUNDS), deepcopy(DEFAULT_BOOKINGS)


def load_json(path: Path, default: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Прочитать список из JSON или вернуть копию значения по умолчанию."""
    if not path.exists():
        return deepcopy(default)
    try:
        with path.open("r", encoding="utf-8") as source:
            data = json.load(source)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Не удалось прочитать файл {path.name}: {error}") from error
    if not isinstance(data, list):
        raise ValueError(f"Файл {path.name} должен содержать список JSON.")
    return data


def save_json(path: Path, data: list[dict[str, Any]]) -> None:
    """Безопасно записать список в JSON через временный файл."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as target:
            json.dump(data, target, ensure_ascii=False, indent=2)
            target.write("\n")
        temporary_path.replace(path)
    except OSError as error:
        if temporary_path.exists():
            temporary_path.unlink()
        raise ValueError(f"Не удалось сохранить файл {path.name}: {error}") from error


def ensure_data_files(data_dir: Path) -> None:
    """Создать отсутствующие файлы с начальными данными."""
    grounds, bookings = default_state()
    grounds_path = data_dir / "grounds.json"
    bookings_path = data_dir / "bookings.json"
    if not grounds_path.exists():
        save_json(grounds_path, grounds)
    if not bookings_path.exists():
        save_json(bookings_path, bookings)


def load_state(data_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Загрузить площадки и бронирования из указанной папки."""
    ensure_data_files(data_dir)
    grounds = load_json(data_dir / "grounds.json", DEFAULT_GROUNDS)
    bookings = load_json(data_dir / "bookings.json", DEFAULT_BOOKINGS)
    return grounds, bookings


def save_state(
    data_dir: Path,
    grounds: list[dict[str, Any]],
    bookings: list[dict[str, Any]],
) -> None:
    """Сохранить площадки и бронирования в два JSON-файла."""
    save_json(data_dir / "grounds.json", grounds)
    save_json(data_dir / "bookings.json", bookings)
