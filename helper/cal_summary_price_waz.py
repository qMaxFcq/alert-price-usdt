from os import getcwd
from sys import path

path.append(getcwd())

from pandas import DataFrame, concat
from database.get_data import get_price_data, get_config_lp_wg
from database.update_data import update_summary_price
from helper.logger import Logger

logger = Logger("cal_summary")


def selected_lp_rate(exchange_id: int):
    try:
        df_usdt_price = get_price_data()
        selected_data = df_usdt_price.loc[
            (df_usdt_price["exchange_id"] == exchange_id)
            & (df_usdt_price["symbol_id"] == 1)
        ]
        return selected_data
    except Exception as e:
        print(f"Error selected_lp : {e}")


def get_rate_p2p_binance():
    try:
        df_usdt_price = get_price_data()
        p2p_rate = df_usdt_price.loc[
            (df_usdt_price["exchange_id"] == 1) & (df_usdt_price["symbol_id"] == 1)
        ]
        return p2p_rate
    except Exception as e:
        print(f"Error get_rate_p2p_binance : {e}")


def cal_summary_price_waz():
    try:
        df_config_lp_wg = get_config_lp_wg().iloc[3]
        exchange_id, dif_buy_sell, is_lp_active, lp_rate = df_config_lp_wg[
            [
                "exchange_id",
                "dif_buy_sell",
                "is_lp_active",
                "lp_rate",
            ]
        ]

        usdt_rate = selected_lp_rate(exchange_id)
        # remark buy_price = bk รับซื้อ, sell_price = bk
        buy_price, sell_price = (
            usdt_rate["buy_price"].iloc[0],
            usdt_rate["sell_price"].iloc[0],
        )

        lp_buy_price, lp_sell_price = sell_price + lp_rate, buy_price - lp_rate

        p2p_binance_rate = get_rate_p2p_binance()
        p2p_buy_price, p2p_sell_price = (
            p2p_binance_rate["buy_price"].iloc[0],
            p2p_binance_rate["sell_price"].iloc[0],
        )

        # filter bk_price and p2p_binance_price
        p2p_buy_price_final = (
            min(lp_buy_price, p2p_buy_price, p2p_buy_price - dif_buy_sell)
            if is_lp_active
            else min(p2p_buy_price, p2p_buy_price - dif_buy_sell)
        )

        p2p_sell_price_final = (
            min(lp_sell_price, p2p_sell_price, p2p_sell_price - dif_buy_sell)
            if is_lp_active
            else min(p2p_sell_price, p2p_sell_price - dif_buy_sell)
        )

        df_p2p_price = DataFrame(
            {
                "id": [5],
                "symbol_id": [1],
                "buy_price": [p2p_buy_price_final],
                "sell_price": [p2p_sell_price_final],
            }
        )
        df_summary = concat([df_p2p_price])
        # print(df_summary)
        update_summary_price(df_summary)

    except Exception as e:
        logger.warn(f"Error from cal_summary: {e}")


if __name__ == "__main__":
    cal_summary_price_waz()
