import asyncio
from pandas import DataFrame, concat
from os import getcwd
from sys import path

path.append(getcwd())
from config.all_config import SYMBOL


def cal_price_xs(price_usdt: DataFrame, exchange_id: DataFrame) -> DataFrame:
    results = []
    result_list = []
    exchange_id = 8

    for symbol in SYMBOL:
        if symbol == "USDT_THB":
            df_buy_price = price_usdt.loc[
                (price_usdt["exchange_id"] == exchange_id)
                & (price_usdt["trade_type"] == "buy")
            ]
            df_sell_price = price_usdt.loc[
                (price_usdt["exchange_id"] == exchange_id)
                & (price_usdt["trade_type"] == "sell")
            ]

            if not df_buy_price.empty and not df_sell_price.empty:
                buy_price, sell_price = (
                    df_sell_price.iloc[0]["price"],
                    df_buy_price.iloc[0]["price"],
                )

                symbol_id = SYMBOL.index(symbol) + 1 if symbol in SYMBOL else None

                # buy คือ เราไปซื้อใน p2p, sell คือ เราไปขายใน p2p
                values = {
                    "exchange_id": exchange_id,
                    "symbol_id": symbol_id,
                    "buy_price": round(float(sell_price), 3),
                    "sell_price": round(float(buy_price), 3),
                }

                result_list.append(DataFrame([values]))

    if result_list:
        final_result = concat(result_list, ignore_index=True)
        results.append(final_result)

    return concat(results, ignore_index=True) if results else None
