from datetime import datetime
from unittest.mock import patch

import pytest

from src.utils import (calculate_cashback, get_exchange_rates, get_greeting, get_stock_info, load_transactions,
                       load_user_settings)

# =======================================
# ====== Тесты load_user_settings =======
# =======================================


def test_load_user_settings(mock_user_file):
    result = load_user_settings("data/user_settings.json")
    assert isinstance(result, dict)
    assert result["user"] == "Анна"
    assert "cards" in result
    assert "portfolio" in result


# ======================================
# ====== Тесты load_transactions =======
# ======================================


def test_load_transactions(mock_transactions_df):
    assert isinstance(mock_transactions_df, list)
    assert len(mock_transactions_df) == 4
    assert mock_transactions_df[0]["Сумма операции"] == -1000.0


def test_load_transactions_real(tmp_path):
    # создаём временный .csv файл
    test_file = tmp_path / "test.csv"
    test_file.write_text("amount;from\n1000;**** 5814\n500;**** 5814", encoding="utf-8")

    result = load_transactions(str(test_file))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["amount"] == 1000


def test_load_transactions_invalid_extension():
    with pytest.raises(ValueError, match="Неподдерживаемый формат файла"):
        load_transactions("file.unsupported")


def test_load_transactions_xlsx(tmp_path):
    import pandas as pd

    test_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"amount": [1000, 500], "from": ["**** 5814", "**** 5814"]})
    df.to_excel(test_file, index=False, engine="openpyxl")

    result = load_transactions(str(test_file))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["amount"] == 1000


# ================================
# ====== Тесты get_greeting ======
# ================================


@pytest.mark.parametrize(
    "name, time, expected_greeting",
    [
        ("Максим", "2025-06-20 01:30:00", "Доброй ночи, Максим!"),
        ("Башир", "2025-06-20 06:05:00", "Доброе утро, Башир!"),
        ("Айгюн", "2025-06-20 13:37:45", "Добрый день, Айгюн!"),
        ("Александра", "2025-06-20 21:30:00", "Добрый вечер, Александра!"),
    ],
)
def test_get_greeting(name, time, expected_greeting):
    time_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    result = get_greeting(name, time_obj)
    assert result == expected_greeting


# =======================================
# ====== Тесты calculate_cashback ======
# =======================================


def test_calculate_cashback(sample_cards, sample_transactions):
    result = calculate_cashback(sample_cards, sample_transactions)
    assert result == {"3456": 15.0, "7654": 5.0}


# =======================================
# ====== Тесты get_exchange_rates =======
# =======================================


@patch("src.utils.requests.get")
def test_get_exchange_rates_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"USD": 91.1, "EUR": 98.9}}

    result = get_exchange_rates(base="RUB", symbols=["USD", "EUR"])
    assert result == {"USD": 91.1, "EUR": 98.9, "RUB": 1}


@patch("src.utils.API_KEY", new=None)
def test_get_exchange_rates_no_api_key():
    result = get_exchange_rates(base="RUB", symbols=["USD", "EUR"])
    assert result == {"USD": 90.0, "EUR": 90.0, "RUB": 1}


@patch("src.utils.API_KEY", new="fake-key")
@patch("src.utils.requests.get", side_effect=Exception("Ошибка запроса"))
def test_get_exchange_rates_error(mock_get):
    result = get_exchange_rates(base="RUB", symbols=["USD"])
    assert result == {"USD": 90.0, "RUB": 1}


# =====================================
# ====== Тесты get_stock_info =========
# =====================================


@pytest.mark.parametrize(
    "portfolio, expected_total",
    [
        ({"AAPL": 1}, 190.0),
        ({"GOOG": 2}, 5600.0),
        ({"TSLA": 3}, 300.0),
    ],
)
def test_get_stock_info(portfolio, expected_total):
    result = get_stock_info(portfolio)
    total = sum(stock["total_value"] for stock in result.values())
    assert total == expected_total
