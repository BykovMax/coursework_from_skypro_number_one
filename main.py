import sys
from pprint import pprint

import pandas as pd

from src.reports import spendings_by_weekday
from src.services import simple_search
from src.utils import load_transactions, load_user_settings
from src.views import homepage_view


def main():
    user = load_user_settings("data/user_settings.json")
    transactions = load_transactions("data/my_operations.xls")
    result = homepage_view("2025-06-20 13:00:00", user, transactions)
    pprint(result)


def run_search():
    transactions = load_transactions("data/other_people's_operations.xlsx")
    search_query = "аптека"  # можно менять
    found = simple_search(search_query, transactions)
    print(f"\n🔎 Найдено транзакций по запросу '{search_query}': {len(found)}")
    pprint(found)


def run_weekday_report():
    df = pd.DataFrame(load_transactions("data/my_operations.csv"))
    result = spendings_by_weekday(df, "2025-06-20")
    print("\n📊 Траты по дням недели (за 30 дней):")
    pprint(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "search":
                run_search()
            case "weekday":
                run_weekday_report()
            case _:
                print("Неизвестный режим")
    else:
        main()
