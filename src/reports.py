# import json
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def spendings_by_weekday(df: pd.DataFrame, date: str | None = None) -> dict:
    """Возвращает суммы трат по дням недели за последние 30 дней."""
    logger.info("Генерация отчёта: траты по дням недели")

    if date:
        end = pd.to_datetime(date)
    else:
        end = pd.Timestamp.today()
    start = end - pd.Timedelta(days=30)

    # Преобразуем даты и суммы
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce", dayfirst=True)
    df["Сумма операции"] = (
        df["Сумма операции"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )

    df_period = df[(df["Дата операции"] >= start) & (df["Дата операции"] <= end)]
    df_period = df_period[df_period["Сумма операции"] < 0].copy()

    # Добавляем колонку с днями недели вручную
    weekday_map = {
        0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг",
        4: "Пятница", 5: "Суббота", 6: "Воскресенье"
    }
    df_period["weekday"] = df_period["Дата операции"].dt.dayofweek.map(weekday_map)

    result = df_period.groupby("weekday")["Сумма операции"].sum().abs().to_dict()

    WEEKDAYS = [
        "Понедельник", "Вторник", "Среда", "Четверг",
        "Пятница", "Суббота", "Воскресенье"
    ]
    result_json_ready = {
        day: round(result[day], 2)
        for day in WEEKDAYS if day in result
    }

    logger.info(f"Отчёт готов: {result_json_ready}")
    return result_json_ready
