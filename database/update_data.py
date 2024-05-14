from os import getcwd
from sys import path

path.append(getcwd())
from database.connection import connect_db, close_connect_db
from pandas import DataFrame, to_datetime, merge
from dateutil.parser import parse
from datetime import timedelta
from helper.logger import Logger


logger = Logger("update_price")


def update_price(price: DataFrame) -> None:
    try:
        connection, cursor = connect_db(), None

        if connection:
            for index, row in price.iterrows():
                exchange_id = row["exchange_id"]
                symbol_id = row["symbol_id"]
                buy_price = row["buy_price"]
                sell_price = row["sell_price"]

                query = f"UPDATE price_data SET buy_price = {buy_price}, sell_price = {sell_price} WHERE exchange_id = {exchange_id} AND symbol_id = {symbol_id}"

                cursor = connection.cursor()
                cursor.execute(query)

                connection.commit()
            logger.info("Data updated successfully")

    except Exception as e:
        logger.warn(f"Error from update_price_table: {e}")
    finally:
        close_connect_db(connection)


def update_timestamp() -> bool:
    try:
        connection, cursor = connect_db(), None
        query = "UPDATE bot_timestamp SET updated_at = now() WHERE id = 3"
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    except Exception as e:
        logger.warn(f"Error from update_timestamp: {e}")
    finally:
        close_connect_db(connection)


def delete_data(new_price: DataFrame):
    try:
        connection, cursor = connect_db(), None
        query = "SELECT * FROM price_history ORDER BY created_at"
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        rows = [
            {
                "exchange_id": int(row[1]),
                "trade_type": str(row[3]),
                "symbol": str(row[4]),
                "created_at": row[9],
            }
            for row in data
        ]
        df = DataFrame(rows)

        df["created_at"] = to_datetime(
            df["created_at"], errors="coerce"
        )  # Use errors='coerce' to handle parsing errors
        new_price["created_at"] = to_datetime(new_price["created_at"], errors="coerce")
        merged_df = merge(
            new_price,
            df,
            on=["exchange_id", "trade_type", "symbol"],
            suffixes=("_new", "_old"),
        )

        time_difference = merged_df["created_at_new"] - merged_df["created_at_old"]
        rows_to_delete = merged_df[time_difference > timedelta(minutes=10)]

        for index, row in rows_to_delete.iterrows():
            delete_query = (
                f"DELETE FROM price_history WHERE exchange_id = {row['exchange_id']} "
                f"AND trade_type = '{row['trade_type']}' "
                f"AND symbol = '{row['symbol']}' "
                f"AND created_at = '{row['created_at_old'].strftime('%Y-%m-%d %H:%M:%S.%f')}'"
            )
            cursor.execute(delete_query)
            # print(
            #     f"Deleted row with exchange_id={row['exchange_id']} and symbol='{row['symbol']}'"
            # )
            connection.commit()

    except Exception as e:
        logger.warn(f"Error from delete_data: {e}")
    finally:
        close_connect_db(connection)


def update_summary_price(price_summary_price: DataFrame):
    try:
        connection, cursor = connect_db(), None
        if connection:
            for index, row in price_summary_price.iterrows():
                id = row["id"]
                buy_price = row["buy_price"]
                sell_price = row["sell_price"]
                query = f"UPDATE price_summary SET buy_price = {buy_price}, sell_price = {sell_price} WHERE id = {id}"
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            logger.info("Data updated summary price successfully")

    except Exception as e:
        print(f"Error from update_summary_price : {e}")
