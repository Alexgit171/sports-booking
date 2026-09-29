"""Вспомогательные функции ввода, преобразования и интроспекции."""

from collections.abc import Callable
from datetime import date
from typing import Any


def parse_int(value: str, minimum: int | None = None, maximum: int | None = None) -> int:
    """Преобразовать строку в целое число с проверкой диапазона."""
    try:
        result = int(value.strip())
    except ValueError as error:
        raise ValueError("Введите целое число.") from error
    if minimum is not None and result < minimum:
        raise ValueError(f"Число должно быть не меньше {minimum}.")
    if maximum is not None and result > maximum:
        raise ValueError(f"Число должно быть не больше {maximum}.")
    return result


def parse_float(
    value: str,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    """Преобразовать строку в число, принимая точку или запятую."""
    try:
        result = float(value.strip().replace(",", "."))
    except ValueError as error:
        raise ValueError("Введите число.") from error
    if minimum is not None and result < minimum:
        raise ValueError(f"Число должно быть не меньше {minimum}.")
    if maximum is not None and result > maximum:
        raise ValueError(f"Число должно быть не больше {maximum}.")
    return result


def parse_date(value: str) -> str:
    """Проверить дату формата ``ГГГГ-ММ-ДД``."""
    clean_value = value.strip()
    try:
        date.fromisoformat(clean_value)
    except ValueError as error:
        raise ValueError("Введите дату в формате ГГГГ-ММ-ДД.") from error
    return clean_value


def read_int(
    prompt: str,
    minimum: int | None = None,
    maximum: int | None = None,
    input_function: Callable[[str], str] = input,
) -> int:
    """Повторять ввод до получения допустимого целого числа."""
    while True:
        try:
            return parse_int(input_function(prompt), minimum, maximum)
        except ValueError as error:
            print(f"Ошибка: {error}")


def read_non_empty(
    prompt: str,
    input_function: Callable[[str], str] = input,
) -> str:
    """Повторять ввод, пока пользователь не введёт непустую строку."""
    while True:
        value = input_function(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не должно быть пустым.")


def inspect_value(value: Any) -> dict[str, Any]:
    """Вернуть учебный результат применения ``type``, ``dir`` и ``hasattr``."""
    public_attributes = [name for name in dir(value) if not name.startswith("_")]
    return {
        "type": type(value).__name__,
        "has_append": hasattr(value, "append"),
        "public_attributes": public_attributes,
    }
