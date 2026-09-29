"""Общие данные для тестов ПР2."""

from copy import deepcopy

import pytest

from storage import DEFAULT_BOOKINGS, DEFAULT_GROUNDS


@pytest.fixture
def grounds():
    """Вернуть независимый список площадок."""
    return deepcopy(DEFAULT_GROUNDS)


@pytest.fixture
def bookings():
    """Вернуть независимый список бронирований."""
    return deepcopy(DEFAULT_BOOKINGS)
