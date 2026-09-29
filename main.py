"""Консольный сервис бронирования спортивных площадок: ПР1 + ПР2.

Автор: Ладинский Александр Владимирович, группа ЭФБО-14-24.

Обычный запуск открывает меню ПР2. Функции ПР1 сохранены, чтобы показать
последовательное развитие проекта и обеспечить совместимость старых тестов.
"""

import os
from pathlib import Path

from bookings import (
    booking_statistics,
    cancel_booking as cancel_saved_booking,
    create_booking as create_saved_booking,
    find_bookings,
    format_booking,
)
from grounds import (
    add_ground,
    filter_grounds,
    find_ground,
    format_ground,
    search_grounds,
    sort_grounds,
)
from storage import load_state, save_state
from utils import inspect_value, parse_date, parse_float, read_int, read_non_empty


# Константы и функции ПР1 оставлены для демонстрации первого этапа.
COURT_NAME = "СпортПарк, площадка для мини-футбола"
BOOKING_DATE_TEXT = "01.10.2026"
HOURLY_RATE = 1500.0
OPEN_HOUR = 8
CLOSE_HOUR = 22
BUSY_START = 18
BUSY_END = 20


def is_slot_available(start_hour: int, duration: int) -> bool:
    """Проверить целочасовой интервал по фиксированному расписанию ПР1."""
    if duration <= 0:
        return False
    end_hour = start_hour + duration
    if start_hour < OPEN_HOUR or end_hour > CLOSE_HOUR:
        return False
    overlaps_busy = start_hour < BUSY_END and end_hour > BUSY_START
    return not overlaps_busy


def calculate_price(duration: int, hourly_rate: float) -> float:
    """Рассчитать стоимость аренды по формуле из ПР1."""
    return duration * hourly_rate


def create_booking(user_name: str, start_hour: int, duration: int) -> str:
    """Сформировать демонстрационное подтверждение или причину отказа ПР1."""
    clean_name = user_name.strip()
    if not clean_name:
        return "Отказ: имя пользователя не должно быть пустым."
    if duration <= 0:
        return "Отказ: длительность должна быть больше нуля."

    end_hour = start_hour + duration
    if start_hour < OPEN_HOUR or end_hour > CLOSE_HOUR:
        return "Отказ: выбранное время выходит за часы работы 08:00-22:00."
    if not is_slot_available(start_hour, duration):
        return "Отказ: выбранное время пересекается с бронью 18:00-20:00."

    total_price = calculate_price(duration, HOURLY_RATE)
    return (
        "Бронирование подтверждено (учебный режим).\n"
        f"Пользователь: {clean_name}\n"
        f"Площадка: {COURT_NAME}\n"
        f"Дата: {BOOKING_DATE_TEXT}\n"
        f"Время: {start_hour:02d}:00-{end_hour:02d}:00\n"
        f"Длительность: {duration} ч.\n"
        f"Стоимость: {total_price:.2f} руб.\n"
        "Заявка показана на экране и не сохраняется."
    )


def main() -> None:
    """Запустить прежний одноразовый сценарий ПР1."""
    print("СЕРВИС БРОНИРОВАНИЯ СПОРТИВНЫХ ПЛОЩАДОК")
    print(f"Площадка: {COURT_NAME}")
    print(f"Учебная дата: {BOOKING_DATE_TEXT}")
    print("Открыто: 08:00-22:00. Занято: 18:00-20:00.")
    print(f"Стоимость часа: {HOURLY_RATE:.2f} руб.")

    user_name = input("Ваше имя: ").strip()
    start_text = input("Час начала (целое число от 8 до 21): ").strip()
    duration_text = input("Длительность в целых часах (от 1 до 14): ").strip()

    if not user_name:
        print("Отказ: имя пользователя не должно быть пустым.")
        return
    if not (
        start_text.isascii()
        and start_text.isdecimal()
        and duration_text.isascii()
        and duration_text.isdecimal()
    ):
        print("Ошибка: введите часы цифрами, например 16 и 2.")
        return
    if len(start_text) > 2 or len(duration_text) > 2:
        print("Ошибка: каждое число должно содержать не более двух цифр.")
        return

    print()
    print(create_booking(user_name, int(start_text), int(duration_text)))


def get_data_directory() -> Path:
    """Вернуть папку данных с учётом переменной окружения для проверок."""
    configured = os.getenv("SPORTS_BOOKING_DATA_DIR")
    return Path(configured) if configured else Path(__file__).parent / "data"


def print_grounds(grounds: list[dict[str, object]]) -> None:
    """Вывести коллекцию площадок."""
    if not grounds:
        print("Площадки не найдены.")
        return
    for ground in grounds:
        print(format_ground(ground))


def print_bookings(
    bookings: list[dict[str, object]],
    grounds: list[dict[str, object]],
) -> None:
    """Вывести коллекцию бронирований вместе с названиями площадок."""
    if not bookings:
        print("Бронирования не найдены.")
        return
    for booking in bookings:
        ground = find_ground(grounds, int(booking["ground_id"]))
        print(format_booking(booking, ground))


def read_float(prompt: str, minimum: float | None = None) -> float:
    """Повторять ввод до получения допустимого вещественного числа."""
    while True:
        try:
            return parse_float(input(prompt), minimum=minimum)
        except ValueError as error:
            print(f"Ошибка: {error}")


def show_menu() -> None:
    """Вывести главное меню ПР2."""
    print(
        "\nПР2 — СЕРВИС БРОНИРОВАНИЯ СПОРТИВНЫХ ПЛОЩАДОК\n"
        "1. Показать площадки\n"
        "2. Добавить площадку\n"
        "3. Найти площадку\n"
        "4. Фильтровать и сортировать площадки\n"
        "5. Создать бронирование\n"
        "6. Найти бронирования пользователя\n"
        "7. Отменить бронирование\n"
        "8. Показать статистику\n"
        "9. Продемонстрировать сценарий ПР1\n"
        "10. Показать интроспекцию коллекции\n"
        "0. Сохранить и выйти"
    )


def add_ground_from_console(grounds: list[dict[str, object]]) -> None:
    """Запросить параметры и добавить площадку в коллекцию."""
    name = read_non_empty("Название: ")
    sport = read_non_empty("Вид спорта: ")
    rate = read_float("Стоимость часа: ", minimum=0.01)
    open_hour = read_int("Час открытия (0–23): ", 0, 23)
    close_hour = read_int("Час закрытия (1–24): ", 1, 24)
    try:
        ground = add_ground(grounds, name, sport, rate, open_hour, close_hour)
    except ValueError as error:
        print(f"Ошибка: {error}")
    else:
        print(f"Добавлено: {format_ground(ground)}")


def filter_grounds_from_console(grounds: list[dict[str, object]]) -> None:
    """Применить генератор фильтрации и сортировку с ``lambda``."""
    sport = input("Вид спорта (Enter — любой): ").strip() or None
    rate_text = input("Максимальная цена (Enter — без ограничения): ").strip()
    try:
        max_rate = parse_float(rate_text, minimum=0.01) if rate_text else None
        result = list(filter_grounds(grounds, sport=sport, max_rate=max_rate))
        print_grounds(sort_grounds(result, key="rate"))
    except ValueError as error:
        print(f"Ошибка: {error}")


def create_booking_from_console(
    grounds: list[dict[str, object]],
    bookings: list[dict[str, object]],
) -> None:
    """Запросить данные и создать сохраняемое бронирование ПР2."""
    print_grounds(grounds)
    user_name = read_non_empty("Имя пользователя: ")
    ground_id = read_int("Номер площадки: ", minimum=1)
    while True:
        try:
            booking_date = parse_date(input("Дата (ГГГГ-ММ-ДД): "))
            break
        except ValueError as error:
            print(f"Ошибка: {error}")
    start_hour = read_int("Час начала: ", 0, 23)
    duration = read_int("Длительность в часах: ", 1, 24)
    try:
        booking = create_saved_booking(
            grounds,
            bookings,
            user_name,
            ground_id,
            booking_date,
            start_hour,
            duration,
        )
    except ValueError as error:
        print(f"Отказ: {error}")
    else:
        ground = find_ground(grounds, ground_id)
        print(f"Бронирование создано: {format_booking(booking, ground)}")


def show_statistics(bookings: list[dict[str, object]]) -> None:
    """Вывести агрегированную статистику бронирований."""
    statistics = booking_statistics(bookings)
    print(
        f'Всего: {statistics["total"]}; '
        f'активных: {statistics["confirmed"]}; '
        f'отменённых: {statistics["cancelled"]}; '
        f'пользователей: {statistics["unique_users"]}; '
        f'выручка: {statistics["revenue"]:.2f} руб.'
    )


def run_application() -> None:
    """Запустить постоянное меню ПР2 с загрузкой и сохранением JSON."""
    data_dir = get_data_directory()
    try:
        grounds, bookings = load_state(data_dir)
    except ValueError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "0":
            save_state(data_dir, grounds, bookings)
            print("Данные сохранены. Работа завершена.")
            return
        if choice == "1":
            print_grounds(grounds)
        elif choice == "2":
            add_ground_from_console(grounds)
            save_state(data_dir, grounds, bookings)
        elif choice == "3":
            print_grounds(search_grounds(grounds, input("Поисковый запрос: ")))
        elif choice == "4":
            filter_grounds_from_console(grounds)
        elif choice == "5":
            create_booking_from_console(grounds, bookings)
            save_state(data_dir, grounds, bookings)
        elif choice == "6":
            query = input("Имя или его часть: ")
            print_bookings(find_bookings(bookings, user_name=query), grounds)
        elif choice == "7":
            booking_id = read_int("Номер бронирования: ", minimum=1)
            try:
                cancel_saved_booking(bookings, booking_id)
                save_state(data_dir, grounds, bookings)
                print("Бронирование отменено.")
            except ValueError as error:
                print(f"Ошибка: {error}")
        elif choice == "8":
            show_statistics(bookings)
        elif choice == "9":
            print(create_booking("Александр", 16, 2))
        elif choice == "10":
            details = inspect_value(grounds)
            print(f'Тип: {details["type"]}; есть append: {details["has_append"]}.')
            print("Первые атрибуты:", ", ".join(details["public_attributes"][:8]))
        else:
            print("Ошибка: выберите существующий пункт меню.")


if __name__ == "__main__":
    run_application()
