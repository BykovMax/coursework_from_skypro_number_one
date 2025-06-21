import json
import logging
from datetime import datetime
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
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce", dayfirst=True)

    # Фильтрация по периоду
    df_period = df[(df["Дата операции"] >= start) & (df["Дата операции"] <= end)]

    # Отдельно только траты
    df_period = df_period[df_period["Сумма операции"] < 0].copy()
    df_period["weekday"] = df_period["Дата операции"].dt.day_name(locale="ru_RU")

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
