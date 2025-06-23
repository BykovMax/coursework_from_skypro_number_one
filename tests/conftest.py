import json
from unittest.mock import mock_open, patch

# import pandas as pd
import pytest


@pytest.fixture
def mock_user_file():
    fake_data = {
        "user": "Анна",
        "cards": [
            {"name": "Visa Classic", "number": "1234567890123456", "cashback_categories": ["супермаркет"]},
            {"name": "Mastercard Black", "number": "9876543210987654", "cashback_categories": ["рестораны"]},
        ],
        "portfolio": {"AAPL": 1, "GOOG": 2},
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(fake_data))):
        yield


@pytest.fixture
def mock_transactions_df():
    return [
        {
            "Номер карты": "*3456",
            "Сумма операции": -1000.0,
            "Дата операции": "2025-06-17 10:00:00",
        },
        {
            "Номер карты": "*3456",
            "Сумма операции": -500.0,
            "Дата операции": "2025-06-18 12:00:00",
        },
        {
            "Номер карты": "*7654",
            "Сумма операции": -200.0,
            "Дата операции": "2025-06-19 14:00:00",
        },
        {
            "Номер карты": "*7654",
            "Сумма операция": -300.0,
            "Дата операции": "2025-06-20 16:00:00",
        },
    ]


@pytest.fixture
def sample_cards():
    return [
        {"name": "Visa Classic", "number": "1234567890123456", "cashback_categories": []},
        {"name": "Mastercard Black", "number": "9876543210987654", "cashback_categories": []},
    ]


@pytest.fixture
def sample_transactions():
    return [
        {"Сумма операции": -1000.0, "Номер карты": "*3456"},
        {"Сумма операции": -500.0, "Номер карты": "*3456"},
        {"Сумма операции": -200.0, "Номер карты": "*7654"},
        {"Сумма операции": -300.0, "Номер карты": "*7654"},
        {"Сумма операции": -100.0, "Номер карты": "*0000"},
    ]


@pytest.fixture
def sample_user():
    return {
        "user": "Максим",
        "cards": [
            {"name": "Visa Classic", "number": "1234567890123456", "balance": 10000},
            {"name": "Mastercard", "number": "9876543210987654", "balance": 5000},
        ],
        "portfolio": {"AAPL": 1, "GOOG": 2, "YNDX": 3},
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL", "GOOG"],
    }
