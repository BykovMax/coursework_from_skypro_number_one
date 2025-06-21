import pytest
from src.services import simple_search


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
