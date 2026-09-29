"""Проверки преобразования ввода и интроспекции."""

import pytest

from utils import (
    inspect_value,
    parse_date,
    parse_float,
    parse_int,
    read_int,
    read_non_empty,
)


def test_parse_int():
    assert parse_int(" 12 ", 1, 20) == 12
    with pytest.raises(ValueError, match="целое"):
        parse_int("1.5")
    with pytest.raises(ValueError, match="не меньше"):
        parse_int("0", minimum=1)
    with pytest.raises(ValueError, match="не больше"):
        parse_int("21", maximum=20)


def test_parse_float():
    assert parse_float(" 1500,50 ", minimum=1) == 1500.5
    with pytest.raises(ValueError, match="Введите число"):
        parse_float("abc")
    with pytest.raises(ValueError, match="не меньше"):
        parse_float("0", minimum=1)


def test_parse_date():
    assert parse_date(" 2026-10-01 ") == "2026-10-01"
    with pytest.raises(ValueError, match="ГГГГ-ММ-ДД"):
        parse_date("01.10.2026")


def test_read_helpers_repeat_after_error(capsys):
    integer_values = iter(["abc", "5"])
    text_values = iter([" ", " Александр "])
    assert read_int("", 1, 10, lambda _: next(integer_values)) == 5
    assert read_non_empty("", lambda _: next(text_values)) == "Александр"
    output = capsys.readouterr().out
    assert output.count("Ошибка:") == 2


def test_inspect_value():
    result = inspect_value([])
    assert result["type"] == "list"
    assert result["has_append"] is True
    assert "append" in result["public_attributes"]
