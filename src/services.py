# import json
import logging
import math
from datetime import datetime

logger = logging.getLogger(__name__)


def simple_search(query: str, transactions: list[dict]) -> list[dict]:
    """Фильтрует транзакции, содержащие подстроку запроса."""
    logger.info(f"Поиск по запросу: '{query}'")

    result = []
    query_lower = query.lower()

    for tx in transactions:
        if any(query_lower in str(value).lower() for value in tx.values()):
            result.append(tx)

    logger.info(f"Найдено совпадений: {len(result)}")
    return result


def investment_bank(month: str, transactions: list[dict], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки, округляя каждую трату до ближайшего значения кратного limit.
    """
    logger.info(f"Расчёт инвесткопилки за {month} с округлением до {limit} ₽")

    total = 0.0
    count = 0

    for tx in transactions:
        date_str = tx.get("Дата операции")
        amount_str = str(tx.get("Сумма операции", "0")).replace(",", ".")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            if date.strftime("%Y-%m") != month:
                continue

            amount = float(amount_str)
            if amount < 0:
                rounded = math.ceil(abs(amount) / limit) * limit
                diff = rounded - abs(amount)
                total += diff
                count += 1

        except Exception as e:
            logger.warning(f"Пропущена транзакция: {tx} — ошибка: {e}")
            continue

    logger.info(f"Всего подходящих транзакций: {count}, сумма к округлению: {round(total, 2)}")
    return round(total, 2)
