import asyncio
from pandas import DataFrame, concat
from os import getcwd
from sys import path
from config.all_config import SYMBOL_BINANCE

path.append(getcwd())


def cal_price_binance(
    price_usdt: DataFrame, price_crypto: DataFrame, exchange: DataFrame
) -> DataFrame:
    results = []
    result_list = []
    exchange_id = 1
    # symbols = ["USDT_THB", "BTC_THB", "ETH_THB", "BNB_THB"]

    for symbol in SYMBOL_BINANCE:
        if symbol == "USDT_THB":
            df_buy_price = price_usdt.loc[
                (price_usdt["exchange_id"] == exchange_id)
                & (price_usdt["trade_type"] == "buy")
            ]
            df_sell_price = price_usdt.loc[
                (price_usdt["exchange_id"] == exchange_id)
                & (price_usdt["trade_type"] == "sell")
            ]
        else:
            df_buy_price = price_crypto.loc[
                (price_crypto["exchange_id"] == exchange_id)
                & (price_crypto["symbol"] == symbol)
                & (price_crypto["trade_type"] == "buy")
            ]
            df_sell_price = price_crypto.loc[
                (price_crypto["exchange_id"] == exchange_id)
                & (price_crypto["symbol"] == symbol)
                & (price_crypto["trade_type"] == "sell")
            ]

        if not df_buy_price.empty and not df_sell_price.empty:
            buy_price, sell_price = (
                df_buy_price.iloc[0]["price"],
                df_sell_price.iloc[0]["price"],
            )

            symbol_id = (
                SYMBOL_BINANCE.index(symbol) + 1 if symbol in SYMBOL_BINANCE else None
            )

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
        # print(final_result)
        results.append(final_result)

    return concat(results, ignore_index=True) if results else None
