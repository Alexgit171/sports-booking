"""Проверки операций с площадками."""

import pytest

from grounds import (
    add_ground,
    filter_grounds,
    find_ground,
    format_ground,
    next_ground_id,
    search_grounds,
    sort_grounds,
)


def test_next_ground_id(grounds):
    assert next_ground_id([]) == 1
    assert next_ground_id(grounds) == 4


def test_add_ground(grounds):
    ground = add_ground(grounds, "  Волейбол Арена ", " волейбол ", 900, 8, 20)
    assert ground["id"] == 4
    assert ground["name"] == "Волейбол Арена"
    assert len(grounds) == 4


def test_add_ground_rejects_empty_fields(grounds):
    with pytest.raises(ValueError, match="не должны быть пустыми"):
        add_ground(grounds, " ", "футбол", 1000, 8, 20)


def test_add_ground_rejects_invalid_rate(grounds):
    with pytest.raises(ValueError, match="Стоимость"):
        add_ground(grounds, "Арена", "футбол", 0, 8, 20)


def test_add_ground_rejects_invalid_hours(grounds):
    with pytest.raises(ValueError, match="Часы работы"):
        add_ground(grounds, "Арена", "футбол", 1000, 20, 8)


def test_find_and_search_grounds(grounds):
    assert find_ground(grounds, 2)["name"] == "Теннис Центр"
    assert find_ground(grounds, 99) is None
    assert [item["id"] for item in search_grounds(grounds, "ТЕННИС")] == [2]
    assert len(search_grounds(grounds, "")) == 3


def test_filter_grounds_is_generator(grounds):
    result = filter_grounds(grounds, max_rate=1500)
    assert iter(result) is result
    assert [item["id"] for item in result] == [1, 2]
    assert [item["id"] for item in filter_grounds(grounds, "баскетбол")] == [3]


def test_sort_and_format_grounds(grounds):
    assert [item["id"] for item in sort_grounds(grounds, "rate")] == [2, 1, 3]
    assert sort_grounds(grounds, "name")[0]["name"] == "Баскет Холл"
    assert "1500.00 руб./ч" in format_ground(grounds[0])
    with pytest.raises(ValueError, match="сортировка"):
        sort_grounds(grounds, "unknown")
