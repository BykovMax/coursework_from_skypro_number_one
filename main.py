import json
import sys
from datetime import datetime
from pprint import pprint

import pandas as pd

from src.reports import spendings_by_weekday
from src.services import investment_bank, simple_search
from src.utils import load_transactions, load_user_settings
from src.views import homepage_view

DATA_FILE_CSV = "data/my_operations.csv"
DATA_FILE_XLS = "data/my_operations.xls"
DATA_FILE_XLSX = "data/other_people's_operations.xlsx"
SETTINGS_FILE = "data/user_settings.json"


def main():
    user = load_user_settings(SETTINGS_FILE)
    transactions = load_transactions(DATA_FILE_XLS)

    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = homepage_view(current_time_str, user, transactions)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def run_search():
    transactions = load_transactions(DATA_FILE_XLSX)
    search_query = "аптека"  # можно менять
    found = simple_search(search_query, transactions)
    print(f"\n🔎 Найдено транзакций по запросу '{search_query}': {len(found)}")
    pprint(found)


def run_weekday_report():
    df = pd.DataFrame(load_transactions(DATA_FILE_CSV))
    result = spendings_by_weekday(df, "2025-06-20")
    print("\n📊 Траты по дням недели (за 30 дней):")
    pprint(result)


def run_investment_mode():
    user = load_user_settings(SETTINGS_FILE)
    limit = user.get("rounding_limit", 50)
    month = user.get("investment_month", "2025-06")

    transactions = load_transactions(DATA_FILE_XLS)
    amount = investment_bank(month, transactions, limit)
    print(f"\n💰 Инвесткопилка: отложено {round(amount, 2)} ₽")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "search":
                run_search()
            case "weekday":
                run_weekday_report()
            case "investment":
                run_investment_mode()
            case _:
                print("Неизвестный режим")
    else:
        main()
