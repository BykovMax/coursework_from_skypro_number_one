from datetime import datetime
from typing import Any, Dict, List

from src.utils import calculate_cashback, get_exchange_rates, get_greeting, get_stock_info


def homepage_view(date_str: str, user: Dict[str, Any], transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для страницы «Главная» на основе переданных данных.
    """
    time_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    greeting = get_greeting(user["user"], time_obj)
    cards = user["cards"]
    cashback_info = calculate_cashback(cards, transactions)
    exchange_rates = get_exchange_rates(base="RUB", symbols=user.get("user_currencies"))
    stock_data = get_stock_info(user["portfolio"], allowed_stocks=user.get("user_stocks"))

    return {
        "greeting": greeting,
        "cards": [
            {
                "name": card["name"],
                "last_digits": card["number"][-4:],
                "balance": card.get("balance", 0),
                "cashback": cashback_info.get(card["number"][-4:], 0),
            }
            for card in cards
        ],
        "search_hint": "поиск по всему Excel-файлу",
        "currency_rates": exchange_rates,
        "stock_prices": stock_data,
    }
