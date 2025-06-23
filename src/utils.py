# import csv
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

# === Настройка логирования ===
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


# === Загрузка переменных окружения ===
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def load_user_settings(path: str) -> Dict[str, Any]:
    """Загружает настройки пользователя из JSON."""
    logger.info(f"Загрузка настроек пользователя из: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_transactions(path: str) -> list[dict]:
    """
    Загружает транзакции из CSV или Excel-файла и возвращает список словарей.
    """
    logger.info(f"Загрузка транзакций из файла: {path}")
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".csv":
        df = pd.read_csv(path, sep=";")
    elif ext == ".xls":
        df = pd.read_excel(path, engine="xlrd")
    elif ext == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    else:
        logger.error(f"Неподдерживаемый формат файла: {ext}")
        raise ValueError(f"Неподдерживаемый формат файла: {ext}")

    return df.to_dict(orient="records")


def get_greeting(name: str, time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = time.hour
    if 6 <= hour < 12:
        part = "Доброе утро"
    elif 12 <= hour < 18:
        part = "Добрый день"
    elif 18 <= hour < 23:
        part = "Добрый вечер"
    else:
        part = "Доброй ночи"
    return f"{part}, {name}!"


def calculate_cashback(cards: List[Dict[str, Any]], transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Рассчитывает кешбэк: 1% от суммы расходов по каждой карте."""
    cashback = {}
    for card in cards:
        card_suffix = str(card["number"])[-4:]
        total_spent = sum(
            abs(float(t.get("Сумма операции", 0)))
            for t in transactions
            if card_suffix in str(t.get("Номер карты", ""))
        )
        cashback[card_suffix] = round(total_spent * 0.01, 2)
    logger.info(f"Кешбэк рассчитан: {cashback}")
    return cashback


def get_exchange_rates(base: str = "RUB", symbols: list[str] = None) -> Dict[str, float]:
    """Получает актуальные курсы валют с помощью API или возвращает заглушку при ошибке."""
    logger.info("Получение курсов валют из API")

    symbols = symbols or ["USD", "EUR"]

    if not API_KEY:
        logger.warning("API-ключ не задан. Возвращается заглушка курсов.")
        return {symbol: 90.0 for symbol in symbols} | {base: 1}

    headers = {"apikey": API_KEY}
    params = {"base": base, "symbols": ",".join(symbols)}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        rates[base] = 1
        return rates
    except Exception as e:
        logger.error(f"Ошибка API. Возвращается заглушка: {e}")
        return {symbol: 90.0 for symbol in symbols} | {base: 1}


def get_stock_info(portfolio: Dict[str, int], allowed_stocks: list[str] = None) -> Dict[str, Any]:
    """Фильтрует портфель по user_stocks и возвращает информацию."""
    logger.info(f"Получение информации по акциям: {portfolio}")
    dummy_prices = {"AAPL": 190.0, "GOOG": 2800.0, "YNDX": 3500.0}

    result = {}
    for stock, qty in portfolio.items():
        if allowed_stocks and stock not in allowed_stocks:
            continue
        price = dummy_prices.get(stock, 100.0)
        result[stock] = {"price": price, "amount": qty, "total_value": round(price * qty, 2)}
    return result
