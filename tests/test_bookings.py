"""Проверки операций с бронированиями."""

import pytest

from bookings import (
    booking_statistics,
    calculate_price,
    cancel_booking,
    create_booking,
    find_bookings,
    format_booking,
    intervals_overlap,
    is_slot_available,
)


def test_calculate_price():
    assert calculate_price(3, 1200.5) == 3601.5


def test_calculate_price_rejects_duration():
    with pytest.raises(ValueError, match="Длительность"):
        calculate_price(0, 1500)


def test_calculate_price_rejects_rate():
    with pytest.raises(ValueError, match="Стоимость"):
        calculate_price(2, -1)


def test_intervals_overlap():
    assert intervals_overlap(17, 19, 18, 20)
    assert intervals_overlap(18, 20, 18, 20)


def test_intervals_touch_without_overlap():
    assert not intervals_overlap(16, 18, 18, 20)
    assert not intervals_overlap(20, 21, 18, 20)


def test_slot_is_available(grounds, bookings):
    assert is_slot_available(grounds[0], bookings, "2026-10-01", 16, 2)


def test_slot_is_unavailable_when_busy(grounds, bookings):
    assert not is_slot_available(grounds[0], bookings, "2026-10-01", 17, 2)


def test_slot_is_unavailable_outside_hours(grounds, bookings):
    assert not is_slot_available(grounds[0], bookings, "2026-10-01", 7, 1)
    assert not is_slot_available(grounds[0], bookings, "2026-10-01", 21, 2)
    assert not is_slot_available(grounds[0], bookings, "2026-10-01", 10, 0)


def test_cancelled_booking_does_not_block_slot(grounds, bookings):
    bookings[0]["status"] = "cancelled"
    assert is_slot_available(grounds[0], bookings, "2026-10-01", 18, 2)


def test_create_booking(grounds, bookings):
    booking = create_booking(
        grounds,
        bookings,
        "  Александр  ",
        1,
        "2026-10-01",
        16,
        2,
    )
    assert booking["id"] == 2
    assert booking["user_name"] == "Александр"
    assert booking["price"] == 3000
    assert "СпортПарк" in format_booking(booking, grounds[0])


def test_create_booking_validates_input(grounds, bookings):
    with pytest.raises(ValueError, match="Имя"):
        create_booking(grounds, bookings, " ", 1, "2026-10-01", 10, 1)
    with pytest.raises(ValueError, match="не найдена"):
        create_booking(grounds, bookings, "Александр", 99, "2026-10-01", 10, 1)
    with pytest.raises(ValueError, match="формат"):
        create_booking(grounds, bookings, "Александр", 1, "01.10.2026", 10, 1)
    with pytest.raises(ValueError, match="недоступно"):
        create_booking(grounds, bookings, "Александр", 1, "2026-10-01", 18, 1)


def test_find_bookings(grounds, bookings):
    create_booking(grounds, bookings, "Александр", 2, "2026-10-02", 10, 1)
    assert len(find_bookings(bookings, user_name="алекс")) == 1
    assert len(find_bookings(bookings, status="confirmed")) == 2
    assert find_bookings(bookings, user_name="нет") == []


def test_cancel_booking(bookings):
    assert cancel_booking(bookings, 1)["status"] == "cancelled"
    with pytest.raises(ValueError, match="уже отменено"):
        cancel_booking(bookings, 1)
    with pytest.raises(ValueError, match="не найдено"):
        cancel_booking(bookings, 99)


def test_booking_statistics(grounds, bookings):
    create_booking(grounds, bookings, "Александр", 2, "2026-10-02", 10, 1)
    cancel_booking(bookings, 1)
    statistics = booking_statistics(bookings)
    assert statistics == {
        "total": 2,
        "confirmed": 1,
        "cancelled": 1,
        "unique_users": 2,
        "revenue": 1200.0,
    }
