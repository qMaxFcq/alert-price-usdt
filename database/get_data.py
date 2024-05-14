from os import getcwd
from sys import path

path.append(getcwd())
from datetime import datetime
from decimal import Decimal
from pandas import DataFrame
from database.connection import connect_db, close_connect_db


def get_usdt_data() -> DataFrame:
    try:
        connection, cursor = connect_db(), None

        if connection:
            query = "SELECT * FROM price_history WHERE (exchange_id, trade_type, created_at) IN (SELECT exchange_id, trade_type, MAX(created_at) FROM price_history WHERE symbol = 'USDT_THB' GROUP BY exchange_id, trade_type) AND symbol = 'USDT_THB' ORDER BY exchange_id"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            columns = [
                "exchange_id",
                "shop_p2p_name",
                "trade_type",
                "symbol",
                "price",
                "min_amount_order",
                "max_amount_order",
                "complete_rate",
                "created_at",
            ]
            df = DataFrame(
                [
                    dict(
                        zip(
                            columns,
                            (
                                int(row[1]),
                                str(row[2]),
                                str(row[3]),
                                str(row[4]),
                                round(float(row[5]), 3),
                                float(row[6]),
                                float(row[7]),
                                float(row[8]),
                                str(row[9]),
                            ),
                        )
                    )
                    for row in data
                ]
            )

            return df
        else:
            print("Error: Unable to establish a database connection.")
            return DataFrame()

    except Exception as e:
        print(f"Error from get_data_db: {e}")
        return DataFrame()
    finally:
        close_connect_db(connection)


def get_crypto_data() -> DataFrame:
    try:
        connection, cursor = connect_db(), None

        if connection is not None:
            query = "SELECT * FROM price_history WHERE symbol IN ('BTC_THB', 'ETH_THB', 'BNB_THB', 'BTC_USDT', 'ETH_USDT', 'BNB_USDT')"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            # print(data)

            rows = [
                {
                    "exchange_id": int(row[1]),
                    "shop_p2p_name": str(row[2]),
                    "trade_type": str(row[3]),
                    "symbol": str(row[4]),
                    "price": float(row[5]),
                    "min_amount_order": float(row[6]),
                    "max_amount_order": float(row[7]),
                    "complete_rate": float(row[8]),
                    "created_at": str(row[9]),
                }
                for row in data
            ]
            df = DataFrame(rows)

            return df
        else:
            print("Error: Unable to establish a database connection.")
            return DataFrame()

    except Exception as e:
        print(f"Error from get_crypto_data: {e}")
        return DataFrame()
    finally:
        close_connect_db(connection)


def get_data_ex() -> DataFrame:
    try:
        connection, cursor = connect_db(), None

        if connection:
            query = "SELECT id, name, fee, offset FROM config_exchange ORDER BY id"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            columns = ["id", "name", "fee", "offset"]
            df_exchange = DataFrame(
                [
                    dict(
                        zip(
                            columns,
                            (
                                int(row[0]),
                                str(row[1]),
                                round(float(row[2]), 3),
                                round(float(row[3]), 3),
                            ),
                        )
                    )
                    for row in data
                ]
            )

            return df_exchange
        else:
            print("Error: Unable to establish a database connection.")
            return DataFrame()

    except Exception as e:
        print(f"Error from get_data_ex: {e}")
        return DataFrame()
    finally:
        close_connect_db(connection)


def get_price_data():
    try:
        connection, cursor = connect_db(), None
        if connection:
            query = "SELECT id, exchange_id, symbol_id, buy_price, sell_price FROM price_data"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            columns = ["id", "exchange_id", "symbol_id", "buy_price", "sell_price"]
            df_price_data = DataFrame(
                [
                    dict(
                        zip(
                            columns,
                            (
                                int(row[0]),
                                int(row[1]),
                                int(row[2]),
                                round(float(row[3]), 3),
                                round(float(row[4]), 3),
                            ),
                        )
                    )
                    for row in data
                ]
            )

            return df_price_data

    except Exception as e:
        print(f"Error from get_price_data: {e}")


def get_config_lp_wg():
    try:
        connection, cursor = connect_db(), None
        if connection:
            query = "SELECT id, lp_rate, shop_rate, exchange_id, is_lp_active, dif_buy_sell, is_using_preset FROM config_lp_wg"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            columns = (
                "id",
                "lp_rate",
                "shop_rate",
                "exchange_id",
                "is_lp_active",
                "dif_buy_sell",
                "is_using_preset",
            )
            df_config_lp_wg = DataFrame(
                [
                    dict(
                        zip(
                            columns,
                            (
                                int(row[0]),
                                round(float(row[1]), 4),
                                round(float(row[2]), 4),
                                int(row[3]),
                                int(row[4]),
                                round(float(row[5]), 4),
                                (row[6]),
                            ),
                        )
                    )
                    for row in data
                ]
            )

            return df_config_lp_wg

    except Exception as e:
        print(f"Error from get_config_lp_wg")


def get_price_summary():
    try:
        connection, cursor = connect_db(), None
        if connection:
            query = "SELECT id, shop_id, type, buy_price, sell_price, preset FROM price_summary"
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()

            columns = (
                "id",
                "shop_id",
                "type",
                "buy_price",
                "sell_price",
                "preset",
                # "dif_buy_sell",
            )

            df_config_price_summary = DataFrame(
                [
                    dict(
                        zip(
                            columns,
                            (
                                int(row[0]),
                                int(row[1]),
                                str(row[2]),
                                round(float(row[3]), 4),
                                round(float(row[4]), 4),
                                int(row[5]),
                            ),
                        )
                    )
                    for row in data
                ]
            )
            return df_config_price_summary

    except Exception as e:
        print(f"Error from get_price_summary", e)


# # Example usage
# result = get_usdt_data()
# result2 = get_crypto_data()
# result3 = get_price_data()
# result4 = get_config_lp_wg()
# get_price_summary()

# print(result)
# print(result2)
# print(result3)
# print(result4)
