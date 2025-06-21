import json
import logging

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
