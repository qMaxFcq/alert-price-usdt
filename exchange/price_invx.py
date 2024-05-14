import asyncio
from pandas import DataFrame, concat
from os import getcwd
from sys import path
from config.all_config import SYMBOL

path.append(getcwd())


def cal_price_invx(
    price_usdt: DataFrame, price_crypto: DataFrame, fee: DataFrame
) -> DataFrame:
    results = []
    result_list = []
    # symbols = ["USDT", "BTC", "ETH", "BNB"]
    exchange_id = 2
    invx_fee = round(float(fee.loc[fee["id"] == exchange_id].iloc[0]["fee"]), 3)

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
            raw_buy_price, raw_sell_price = (
                df_buy_price.iloc[0]["price"],
                df_sell_price.iloc[0]["price"],
            )

            feebuy, feesell = (
                round(raw_buy_price * invx_fee, 2),
                round(raw_sell_price * invx_fee, 2),
            )
            buy_after_fee, sell_after_fee = (
                raw_buy_price - feebuy,
                raw_sell_price + feesell,
            )

            df_buy_price.loc[:, "price"] = buy_after_fee
            df_sell_price.loc[:, "price"] = sell_after_fee
            symbol_id = SYMBOL.index(symbol) + 1 if symbol in SYMBOL else None

            values = {
                "exchange_id": exchange_id,
                "symbol_id": symbol_id,
                "buy_price": round(float(buy_after_fee), 3),
                "sell_price": round(float(sell_after_fee), 3),
            }

            result_list.append(DataFrame([values]))

    if result_list:
        final_result = concat(result_list, ignore_index=True)
        results.append(final_result)

    return concat(results, ignore_index=True) if results else None
