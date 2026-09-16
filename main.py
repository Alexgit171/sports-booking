"""ПР1. Сервис бронирования спортивных площадок.

Автор: Ладинский Александр Владимирович, ЭФБО-14-24.
Один запуск демонстрирует оформление одной заявки без сохранения данных.
"""

from datetime import date


COURT_NAME = "СпортПарк, площадка для мини-футбола"
BOOKING_DATE = date(2026, 10, 1)
HOURLY_RATE = 1500.0
OPEN_HOUR = 8
CLOSE_HOUR = 22
BUSY_START = 18
BUSY_END = 20


def is_slot_available(start_hour, duration):
    """Проверить целочасовой интервал по расписанию площадки."""
    if duration <= 0:
        return False

    end_hour = start_hour + duration
    if start_hour < OPEN_HOUR or end_hour > CLOSE_HOUR:
        return False

    overlaps_busy = start_hour < BUSY_END and end_hour > BUSY_START
    return not overlaps_busy


def calculate_price(duration, hourly_rate):
    """Рассчитать стоимость для положительной длительности и тарифа."""
    return duration * hourly_rate


def create_booking(user_name, start_hour, duration):
    """Сформировать демонстрационное подтверждение или причину отказа."""
    user_name = user_name.strip()
    if not user_name:
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
        f"Пользователь: {user_name}\n"
        f"Площадка: {COURT_NAME}\n"
        f"Дата: {BOOKING_DATE:%d.%m.%Y}\n"
        f"Время: {start_hour:02d}:00-{end_hour:02d}:00\n"
        f"Длительность: {duration} ч.\n"
        f"Стоимость: {total_price:.2f} руб.\n"
        "Заявка показана на экране и не сохраняется."
    )


def main():
    """Получить данные пользователя и вывести результат заявки."""
    print("СЕРВИС БРОНИРОВАНИЯ СПОРТИВНЫХ ПЛОЩАДОК")
    print(f"Площадка: {COURT_NAME}")
    print(f"Учебная дата: {BOOKING_DATE:%d.%m.%Y}")
    print("Открыто: 08:00-22:00. Занято: 18:00-20:00.")
    print(f"Стоимость часа: {HOURLY_RATE:.2f} руб.")

    user_name = input("Ваше имя: ").strip()
    start_text = input("Час начала (целое число от 8 до 21): ").strip()
    duration_text = input("Длительность в целых часах (от 1 до 14): ").strip()

    if not user_name:
        print("Отказ: имя пользователя не должно быть пустым.")
        return
    if not (
        start_text.isascii() and start_text.isdecimal()
        and duration_text.isascii() and duration_text.isdecimal()
    ):
        print("Ошибка: введите часы цифрами, например 16 и 2.")
        return
    if len(start_text) > 2 or len(duration_text) > 2:
        print("Ошибка: каждое число должно содержать не более двух цифр.")
        return

    start_hour = int(start_text)
    duration = int(duration_text)
    print()
    print(create_booking(user_name, start_hour, duration))


if __name__ == "__main__":
    main()
