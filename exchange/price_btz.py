import asyncio
from pandas import DataFrame, concat
from os import getcwd
from sys import path

path.append(getcwd())
from config.all_config import SYMBOL


def cal_price_btz(price_usdt: DataFrame, exchange: DataFrame) -> DataFrame:
    results = []
    result_list = []
    exchange_id = 4
    # symbols = ["USDT"]

    for symbol in SYMBOL:
        if symbol == "USDT_THB":
            df_price = price_usdt.loc[
                (price_usdt["exchange_id"] == exchange_id)
                & (price_usdt["trade_type"] == "mid")
            ]
            df_exchange = exchange.loc[(exchange["id"] == exchange_id)]
            offset = df_exchange.iloc[0]["offset"]
            # df_sell_price = price_usdt.loc[(price_usdt['exchange_id'] == exchange_id) & (
            #     price_usdt['trade_type'] == 'sell')]

            if not df_price.empty:
                buy_price, sell_price = (
                    df_price.iloc[0]["price"] + offset,
                    df_price.iloc[0]["price"] - offset,
                )

                symbol_id = SYMBOL.index(symbol) + 1 if symbol in SYMBOL else None

                values = {
                    "exchange_id": exchange_id,
                    "symbol_id": symbol_id,
                    "buy_price": round(float(buy_price), 3),
                    "sell_price": round(float(sell_price), 3),
                }

                result_list.append(DataFrame([values]))

    if result_list:
        final_result = concat(result_list, ignore_index=True)
        results.append(final_result)

    return concat(results, ignore_index=True) if results else None
