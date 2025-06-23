from unittest.mock import patch

import pytest

from src.views import homepage_view


@pytest.mark.parametrize(
    "date_str, expected_greeting",
    [
        ("2025-06-20 01:00:00", "Доброй ночи, Максим!"),
        ("2025-06-20 07:30:00", "Доброе утро, Максим!"),
        ("2025-06-20 14:45:00", "Добрый день, Максим!"),
        ("2025-06-20 20:15:00", "Добрый вечер, Максим!"),
    ],
)
@patch("src.views.get_exchange_rates", return_value={"USD": 90.0, "RUB": 1})
@patch(
    "src.views.get_stock_info",
    return_value={
        "AAPL": {"price": 190.0, "amount": 1, "total_value": 190.0},
        "GOOG": {"price": 2800.0, "amount": 2, "total_value": 5600.0},
    },
)
def test_homepage_view_pure_logic(
    mock_stocks, mock_rates, date_str, expected_greeting, sample_user, sample_transactions
):
    result = homepage_view(date_str, sample_user, sample_transactions)

    assert result["greeting"] == expected_greeting
    assert set(result["currency_rates"].keys()) == {"USD", "RUB"}
    assert set(result["stock_prices"].keys()) == {"AAPL", "GOOG"}

    for card in result["cards"]:
        assert "name" in card
        assert "last_digits" in card
        assert "balance" in card
        assert "cashback" in card
