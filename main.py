from pprint import pprint

from src.utils import load_user_settings, load_transactions
from src.views import homepage_view


def main():
    user = load_user_settings("data/user_settings.json")
    transactions = load_transactions("data/operations.xls")
    result = homepage_view("2025-06-20 13:00:00", user, transactions)
    pprint(result)


if __name__ == "__main__":
    main()