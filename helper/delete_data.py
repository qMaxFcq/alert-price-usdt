from os import getcwd
from sys import path
from pandas import concat

path.append(getcwd())

#### Local ####
from database.get_data import get_usdt_data, get_crypto_data
from database.update_data import delete_data
from helper.logger import Logger

logger = Logger("delete_data")


def check_and_delete():
    try:
        df_usdt_price = get_usdt_data()
        df_usdt_price = df_usdt_price[
            ["exchange_id", "trade_type", "symbol", "created_at"]
        ]

        selected_rows = df_usdt_price[df_usdt_price["exchange_id"].isin([1, 5])]
        # print(selected_rows)
        delete_data(selected_rows)

    except Exception as err:
        logger.warn(f"Error from check_and_delete : {err}")
