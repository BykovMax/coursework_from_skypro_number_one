# Финальный проект: Финансовый помощник

## 📄 Описание

Приложение для анализа личных финансов, построенное на Python. Обрабатывает Excel-файл с транзакциями и формирует отчёты, рекомендации и API-ответы с курсов валют и инвестиционной информацией.

## 🚀 Запуск

1. Установить зависимости:
```bash
poetry install
```

2. Создать файл `.env` с API-ключом:
```
EXCHANGE_API_KEY=your_api_key
```

3. Запустить основной модуль:
```bash
python main.py
```

## ⚙️ Режимы запуска (main.py)

| Команда                       | Что делает                                  |
|-------------------------------|----------------------------------------------|
| `python main.py`              | запуск страницы «Главная»                   |
| `python main.py search`       | поиск по транзакциям (simple_search)         |


## 🧪 Тесты

```bash
pytest --cov
coverage html
```

## 🌐 Используемое API

- [https://apilayer.com/marketplace/exchangerates_data-api](https://apilayer.com/marketplace/exchangerates_data-api)

## 📸 Скриншот результата

![Пример](images/example_output.png)

## 🧾 Пример JSON-ответа

```json
{
  "greeting": "Доброе утро, Максим!",
  "cards": [
    {
      "name": "Visa Classic",
      "last_digits": "3456",
      "balance": 10000,
      "cashback": 12.5
    }
  ],
  "search_hint": "поиск по всему Excel-файлу",
  "currency_rates": {
    "USD": 89.5,
    "EUR": 96.2,
    "RUB": 1
  },
  "stock_prices": {
    "AAPL": {
      "price": 190.0,
      "amount": 5,
      "total_value": 950.0
    }
  }
}
```

## 📁 Структура проекта

- `src/` — бизнес-логика
- `tests/` — тесты с параметризацией, фикстурами, mock
- `data/` — входные данные (`user_settings.json`, `operations.xls`)

## 🧰 Универсальный шаблон user_settings.json

```json
{
  "user": "Имя",
  "cards": [
    {
      "name": "Название карты",
      "number": "0000111122223456",
      "cashback_categories": ["супермаркет", "аптека"],
      "balance": 10000
    }
  ],
  "portfolio": {
    "AAPL": 5,
    "GOOG": 2
  },
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "GOOG"]
}
```
