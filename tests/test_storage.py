"""Проверки JSON-хранилища."""

import json

import pytest

from storage import (
    DEFAULT_GROUNDS,
    default_state,
    ensure_data_files,
    load_json,
    load_state,
    save_json,
    save_state,
)


def test_default_state_returns_independent_copies():
    first_grounds, _ = default_state()
    second_grounds, _ = default_state()
    first_grounds[0]["name"] = "Изменено"
    assert second_grounds[0]["name"] != "Изменено"


def test_save_and_load_json(tmp_path):
    path = tmp_path / "nested" / "data.json"
    save_json(path, [{"тест": "данные"}])
    assert load_json(path, []) == [{"тест": "данные"}]
    assert not path.with_suffix(".json.tmp").exists()


def test_load_json_uses_default_for_missing_file(tmp_path):
    loaded = load_json(tmp_path / "missing.json", DEFAULT_GROUNDS)
    loaded[0]["name"] = "Изменено"
    assert DEFAULT_GROUNDS[0]["name"] != "Изменено"


def test_load_json_rejects_invalid_content(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{не json}", encoding="utf-8")
    with pytest.raises(ValueError, match="Не удалось прочитать"):
        load_json(invalid, [])

    not_a_list = tmp_path / "object.json"
    not_a_list.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(ValueError, match="список"):
        load_json(not_a_list, [])


def test_ensure_load_and_save_state(tmp_path):
    ensure_data_files(tmp_path)
    grounds, bookings = load_state(tmp_path)
    assert len(grounds) == 3
    assert len(bookings) == 1
    grounds[0]["name"] = "Новое название"
    save_state(tmp_path, grounds, bookings)
    reloaded_grounds, _ = load_state(tmp_path)
    assert reloaded_grounds[0]["name"] == "Новое название"
