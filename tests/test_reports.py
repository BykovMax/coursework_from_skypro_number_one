import pandas as pd
import pytest

from src.reports import spendings_by_weekday

# ==============================================
# ====== Тесты spendings_by_weekday (отчёт) =====
# ==============================================


@pytest.mark.parametrize(
    "date, expected_days",
    [
        ("2025-06-20", {"Вторник", "Среда", "Четверг"}),
        (None, set()),  # <- фикс!
    ],
)
def test_spendings_by_weekday(mock_transactions_df, date, expected_days):
    df = pd.DataFrame(mock_transactions_df)
    result = spendings_by_weekday(df, date)

    assert isinstance(result, dict)
    assert all(isinstance(k, str) and isinstance(v, float | int) for k, v in result.items())
    if expected_days:
        assert set(result.keys()).issuperset(expected_days)
