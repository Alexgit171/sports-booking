"""Операции с бронированиями спортивных площадок."""

from collections.abc import Iterable
from datetime import date
from typing import Any

from grounds import Ground, find_ground


Booking = dict[str, Any]


def calculate_price(duration: int, hourly_rate: float) -> float:
    """Рассчитать стоимость аренды и проверить исходные значения."""
    if duration <= 0:
        raise ValueError("Длительность должна быть больше нуля.")
    if hourly_rate <= 0:
        raise ValueError("Стоимость часа должна быть больше нуля.")
    return round(duration * hourly_rate, 2)


def intervals_overlap(
    first_start: int,
    first_end: int,
    second_start: int,
    second_end: int,
) -> bool:
    """Проверить пересечение двух полуоткрытых интервалов времени."""
    return first_start < second_end and first_end > second_start


def validate_date(booking_date: str) -> str:
    """Проверить дату ISO ``ГГГГ-ММ-ДД`` и вернуть исходную строку."""
    try:
        date.fromisoformat(booking_date)
    except ValueError as error:
        raise ValueError("Дата должна иметь формат ГГГГ-ММ-ДД.") from error
    return booking_date


def is_slot_available(
    ground: Ground,
    bookings: Iterable[Booking],
    booking_date: str,
    start_hour: int,
    duration: int,
    ignore_booking_id: int | None = None,
) -> bool:
    """Проверить часы работы и отсутствие пересекающихся активных броней."""
    validate_date(booking_date)
    if duration <= 0:
        return False

    end_hour = start_hour + duration
    if start_hour < int(ground["open_hour"]) or end_hour > int(ground["close_hour"]):
        return False

    for booking in bookings:
        if booking.get("status") != "confirmed":
            continue
        if int(booking["ground_id"]) != int(ground["id"]):
            continue
        if booking["date"] != booking_date:
            continue
        if ignore_booking_id is not None and int(booking["id"]) == ignore_booking_id:
            continue
        if intervals_overlap(
            start_hour,
            end_hour,
            int(booking["start_hour"]),
            int(booking["end_hour"]),
        ):
            return False
    return True


def next_booking_id(bookings: Iterable[Booking]) -> int:
    """Вернуть следующий идентификатор бронирования."""
    return max((int(booking["id"]) for booking in bookings), default=0) + 1


def create_booking(
    grounds: Iterable[Ground],
    bookings: list[Booking],
    user_name: str,
    ground_id: int,
    booking_date: str,
    start_hour: int,
    duration: int,
) -> Booking:
    """Создать подтверждённое бронирование или вызвать ``ValueError``."""
    clean_name = user_name.strip()
    if not clean_name:
        raise ValueError("Имя пользователя не должно быть пустым.")

    ground = find_ground(grounds, ground_id)
    if ground is None:
        raise ValueError("Площадка с таким идентификатором не найдена.")
    validate_date(booking_date)
    if duration <= 0:
        raise ValueError("Длительность должна быть больше нуля.")
    if not is_slot_available(ground, bookings, booking_date, start_hour, duration):
        raise ValueError("Выбранное время недоступно или выходит за часы работы.")

    booking: Booking = {
        "id": next_booking_id(bookings),
        "user_name": clean_name,
        "ground_id": ground_id,
        "date": booking_date,
        "start_hour": start_hour,
        "end_hour": start_hour + duration,
        "duration": duration,
        "price": calculate_price(duration, float(ground["hourly_rate"])),
        "status": "confirmed",
    }
    bookings.append(booking)
    return booking


def find_bookings(
    bookings: Iterable[Booking],
    user_name: str | None = None,
    status: str | None = None,
) -> list[Booking]:
    """Найти бронирования по части имени и/или статусу."""
    normalized_name = user_name.strip().casefold() if user_name else None
    return [
        booking
        for booking in bookings
        if (
            normalized_name is None
            or normalized_name in str(booking["user_name"]).casefold()
        )
        and (status is None or booking["status"] == status)
    ]


def cancel_booking(bookings: Iterable[Booking], booking_id: int) -> Booking:
    """Отменить активное бронирование и вернуть изменённую запись."""
    booking = next(
        (item for item in bookings if int(item["id"]) == booking_id),
        None,
    )
    if booking is None:
        raise ValueError("Бронирование с таким идентификатором не найдено.")
    if booking["status"] == "cancelled":
        raise ValueError("Бронирование уже отменено.")
    booking["status"] = "cancelled"
    return booking


def booking_statistics(bookings: Iterable[Booking]) -> dict[str, int | float]:
    """Посчитать количество заявок, пользователей и активную выручку."""
    booking_list = list(bookings)
    confirmed = [item for item in booking_list if item["status"] == "confirmed"]
    return {
        "total": len(booking_list),
        "confirmed": len(confirmed),
        "cancelled": sum(item["status"] == "cancelled" for item in booking_list),
        "unique_users": len(
            {str(item["user_name"]).strip().casefold() for item in booking_list}
        ),
        "revenue": round(sum(float(item["price"]) for item in confirmed), 2),
    }


def format_booking(booking: Booking, ground: Ground | None = None) -> str:
    """Подготовить бронирование для вывода в консоль."""
    ground_name = str(ground["name"]) if ground else f'площадка #{booking["ground_id"]}'
    status = "подтверждено" if booking["status"] == "confirmed" else "отменено"
    return (
        f'#{booking["id"]} {booking["user_name"]}; {ground_name}; '
        f'{booking["date"]} {int(booking["start_hour"]):02d}:00–'
        f'{int(booking["end_hour"]):02d}:00; {float(booking["price"]):.2f} руб.; '
        f'{status}'
    )
