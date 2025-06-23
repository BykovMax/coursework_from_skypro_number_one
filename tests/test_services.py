import pytest

from src.services import investment_bank, simple_search

# ===============================
# ====== Тесты simple_search =====
# ===============================


@pytest.fixture
def sample_transactions():
    return [
        {"Описание": "Магнит у дома", "Сумма": -500, "Категория": "Супермаркеты"},
        {"Описание": "Перевод Иванову", "Сумма": -1000, "Категория": "Переводы"},
        {"Описание": "Аптека Вита", "Сумма": -200, "Категория": "Аптеки"},
        {"Описание": "Зарплата", "Сумма": 50000, "Категория": "Доход"},
    ]


@pytest.mark.parametrize(
    "query, expected_count",
    [
        ("магнит", 1),
        ("аптека", 1),
        ("перевод", 1),
        ("зарплата", 1),
        ("нет такого", 0),
    ],
)
def test_simple_search(query, expected_count, sample_transactions):
    result = simple_search(query, sample_transactions)
    assert isinstance(result, list)
    assert len(result) == expected_count


# ============================================
# ====== Тесты для функции investment_bank ===
# ============================================


@pytest.mark.parametrize(
    "month, limit, expected_amount",
    [
        ("2025-06", 50, 96.0),
        ("2025-06", 100, 246.0),
        ("2025-06", 10, 16),
        ("2025-05", 50, 0.0),  # нет транзакций в этом месяце
    ]
)
def test_investment_bank(mock_transactions_df, month, limit, expected_amount):
    result = investment_bank(month, mock_transactions_df, limit)
    assert isinstance(result, float)
    assert round(result, 2) == expected_amount


def test_investment_bank_with_invalid_date():
    transactions = [
        {"Дата операции": "некорректно", "Сумма операции": "-300.00"},
        {"Дата операции": "2025-06-10 12:00:00", "Сумма операции": "-500.00"},
    ]
    result = investment_bank("2025-06", transactions, 50)
    assert isinstance(result, float)
    assert result == 0.0  # проверяем, что хотя бы одна строка обработалась
