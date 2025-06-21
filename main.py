import sys
from pprint import pprint

from src.utils import load_user_settings, load_transactions
from src.views import homepage_view
from src.services import simple_search


def main():
    user = load_user_settings("data/user_settings.json")
    transactions = load_transactions("data/operations.xls")
    result = homepage_view("2025-06-20 13:00:00", user, transactions)
    pprint(result)


def run_search():
    transactions = load_transactions("data/operations.xls")
    search_query = "супермаркет"  # можно менять
    found = simple_search(search_query, transactions)
    print(f"\n🔎 Найдено транзакций по запросу '{search_query}': {len(found)}")
    pprint(found)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        run_search()
    else:
        main()