"""Вспомогательные проверки; запуск: python -m unittest -v."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from main import calculate_price, create_booking, is_slot_available, main


class BookingTests(unittest.TestCase):
    def test_free_interval(self):
        self.assertTrue(is_slot_available(10, 2))

    def test_end_at_busy_start(self):
        self.assertTrue(is_slot_available(16, 2))

    def test_start_at_busy_end(self):
        self.assertTrue(is_slot_available(20, 2))

    def test_busy_intersections(self):
        for start, duration in ((17, 2), (18, 1), (19, 2), (16, 5)):
            with self.subTest(start=start, duration=duration):
                self.assertFalse(is_slot_available(start, duration))

    def test_opening_boundary(self):
        self.assertTrue(is_slot_available(8, 1))
        self.assertFalse(is_slot_available(7, 1))

    def test_closing_boundary(self):
        self.assertTrue(is_slot_available(21, 1))
        self.assertFalse(is_slot_available(21, 2))
        self.assertFalse(is_slot_available(22, 1))

    def test_nonpositive_duration(self):
        self.assertFalse(is_slot_available(10, 0))
        self.assertFalse(is_slot_available(10, -1))

    def test_price(self):
        self.assertEqual(calculate_price(2, 1500.0), 3000.0)
        self.assertEqual(calculate_price(3, 1200.5), 3601.5)

    def test_confirmation(self):
        result = create_booking("  Александр  ", 16, 2)
        self.assertIn("Пользователь: Александр\n", result)
        self.assertIn("16:00-18:00", result)
        self.assertIn("3000.00 руб.", result)
        self.assertIn("01.10.2026", result)

    def test_empty_name(self):
        self.assertIn("имя", create_booking("   ", 16, 2))
        self.assertNotIn("подтверждено", create_booking("", 16, 2))

    def test_rejection_reasons(self):
        self.assertIn("пересекается", create_booking("Александр", 17, 2))
        self.assertIn("часы работы", create_booking("Александр", 7, 1))
        self.assertIn("больше нуля", create_booking("Александр", 10, 0))

    def test_console_success(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["Александр", "16", "2"]):
            with redirect_stdout(output):
                main()
        self.assertIn("3000.00 руб.", output.getvalue())

    def test_console_invalid_numbers(self):
        for value in ("abc", "", "1.5", "-1", "²", "9" * 100):
            with self.subTest(value=value):
                output = io.StringIO()
                with patch("builtins.input", side_effect=["Александр", value, "2"]):
                    with redirect_stdout(output):
                        main()
                self.assertIn("Ошибка:", output.getvalue())
                self.assertNotIn("подтверждено", output.getvalue())


if __name__ == "__main__":
    unittest.main()
