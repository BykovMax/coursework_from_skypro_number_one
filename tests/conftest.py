import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest


@pytest.fixture
def mock_user_file():
    fake_data = {
        "user": "Анна",
        "cards": [
            {
                "name": "Visa Classic",
                "number": "1234567890123456",
                "cashback_categories": ["супермаркет"]
            },
            {
                "name": "Mastercard Black",
                "number": "9876543210987654",
                "cashback_categories": ["рестораны"]
            }
        ],
        "portfolio": {
            "AAPL": 1,
            "GOOG": 2
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(fake_data))):
        yield


@pytest.fixture
def mock_transactions_df():
    df = pd.DataFrame({
        "Сумма операции": [-1000.0, -500.0, -200.0, -300.0],
        "Номер карты": ["*3456", "*3456", "*7654", "*7654"]
    })
    with patch("pandas.read_csv", return_value=df), \
         patch("pandas.read_excel", return_value=df):
        yield df.to_dict(orient="records")


@pytest.fixture
def sample_cards():
    return [
        {"name": "Visa Classic", "number": "1234567890123456", "cashback_categories": []},
        {"name": "Mastercard Black", "number": "9876543210987654", "cashback_categories": []}
    ]


@pytest.fixture
def sample_transactions():
    return [
        {"Сумма операции": -1000.0, "Номер карты": "*3456"},
        {"Сумма операции": -500.0, "Номер карты": "*3456"},
        {"Сумма операции": -200.0, "Номер карты": "*7654"},
        {"Сумма операции": -300.0, "Номер карты": "*7654"},
        {"Сумма операции": -100.0, "Номер карты": "*0000"}
    ]

@pytest.fixture
def sample_user():
    return {
        "user": "Максим",
        "cards": [
            {"name": "Visa Classic", "number": "1234567890123456", "balance": 10000},
            {"name": "Mastercard", "number": "9876543210987654", "balance": 5000}
        ],
        "portfolio": {"AAPL": 1, "GOOG": 2, "YNDX": 3},
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL", "GOOG"]
    }