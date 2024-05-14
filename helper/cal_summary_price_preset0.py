from os import getcwd
from sys import path

path.append(getcwd())

from pandas import DataFrame, concat
from database.get_data import get_price_summary, get_config_lp_wg, get_price_data
from database.update_data import update_summary_price
from helper.logger import Logger

logger = Logger("cal_summary")


def get_rate_p2p_binance():
    try:
        df_usdt_price = get_price_data()
        p2p_rate = df_usdt_price.loc[
            (df_usdt_price["exchange_id"] == 1) & (df_usdt_price["symbol_id"] == 1)
        ]
        return p2p_rate
    except Exception as e:
        print(f"Error get_rate_p2p_binance : {e}")


def get_price_from_summary():
    try:
        df_price_summary = get_price_summary()
        selected_data = df_price_summary.loc[
            (df_price_summary["shop_id"] == 1) & (df_price_summary["preset"] != 0)
        ]
        return selected_data
    except Exception as e:
        print(f"Error get_price_summary : {e}")


def get_lp_active():
    try:
        df_lp_active = get_config_lp_wg()

        return df_lp_active
    except Exception as e:
        print(f"Error get_price_summary : {e}")


def cal_summary_preset0():
    try:
        df_price_summary = get_price_from_summary()
        df_lp_active = get_lp_active()
        p2p_binance_rate = get_rate_p2p_binance()
        p2p_buy_price, p2p_sell_price = (
            p2p_binance_rate["buy_price"].iloc[0],
            p2p_binance_rate["sell_price"].iloc[0],
        )

        df_preset_1 = df_lp_active.loc[0]
        is_using_preset_1 = df_preset_1["is_using_preset"]

        if is_using_preset_1 == 1.0:

            # get price wg from preset 1
            df_price_summary_wg = df_price_summary.loc[0]
            wg_buy_price = df_price_summary_wg["buy_price"]
            wg_sell_price = df_price_summary_wg["sell_price"]

            # get price lp from preset 1
            df_price_summary_lp = df_price_summary.loc[1]
            lp_buy_price = df_price_summary_lp["buy_price"]
            lp_sell_price = df_price_summary_lp["sell_price"]

            df_wg_price = DataFrame(
                {
                    "id": [8],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_lp_price = DataFrame(
                {
                    "id": [9],
                    "symbol_id": [1],
                    "buy_price": [lp_buy_price],
                    "sell_price": [lp_sell_price],
                }
            )

            df_p2p_price = DataFrame(
                {
                    "id": [10],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_summary = concat([df_wg_price, df_lp_price, df_p2p_price])
            # print(df_summary)
            update_summary_price(df_summary)

        df_preset_2 = df_lp_active.loc[4]
        is_using_preset_2 = df_preset_2["is_using_preset"]

        if is_using_preset_2 == 1.0:

            # get price wg from preset 2
            df_price_summary_wg = df_price_summary.loc[9]
            wg_buy_price = df_price_summary_wg["buy_price"]
            wg_sell_price = df_price_summary_wg["sell_price"]

            # get price lp from preset 2
            df_price_summary_lp = df_price_summary.loc[10]
            lp_buy_price = df_price_summary_lp["buy_price"]
            lp_sell_price = df_price_summary_lp["sell_price"]

            df_wg_price = DataFrame(
                {
                    "id": [8],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_lp_price = DataFrame(
                {
                    "id": [9],
                    "symbol_id": [1],
                    "buy_price": [lp_buy_price],
                    "sell_price": [lp_sell_price],
                }
            )

            df_p2p_price = DataFrame(
                {
                    "id": [10],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_summary = concat([df_wg_price, df_lp_price, df_p2p_price])
            # print(df_summary)
            update_summary_price(df_summary)

        df_preset_3 = df_lp_active.loc[5]
        is_using_preset_3 = df_preset_3["is_using_preset"]

        if is_using_preset_3 == 1.0:

            # get price wg from preset 3
            df_price_summary_wg = df_price_summary.loc[12]
            wg_buy_price = df_price_summary_wg["buy_price"]
            wg_sell_price = df_price_summary_wg["sell_price"]

            # get price lp from preset 3
            df_price_summary_lp = df_price_summary.loc[13]
            lp_buy_price = df_price_summary_lp["buy_price"]
            lp_sell_price = df_price_summary_lp["sell_price"]

            df_wg_price = DataFrame(
                {
                    "id": [8],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_lp_price = DataFrame(
                {
                    "id": [9],
                    "symbol_id": [1],
                    "buy_price": [lp_buy_price],
                    "sell_price": [lp_sell_price],
                }
            )

            df_p2p_price = DataFrame(
                {
                    "id": [10],
                    "symbol_id": [1],
                    "buy_price": [wg_buy_price],
                    "sell_price": [wg_sell_price],
                }
            )

            df_summary = concat([df_wg_price, df_lp_price, df_p2p_price])
            # print(df_summary)
            update_summary_price(df_summary)

        if is_using_preset_1 == 0 and is_using_preset_2 == 0 and is_using_preset_3 == 0:

            # get price wg from preset 1
            df_price_summary_wg_1 = df_price_summary.loc[0]
            wg_buy_price_1 = df_price_summary_wg_1["buy_price"]
            wg_sell_price_1 = df_price_summary_wg_1["sell_price"]

            # get price lp from preset 1
            df_price_summary_lp_1 = df_price_summary.loc[1]
            lp_buy_price_1 = df_price_summary_lp_1["buy_price"]
            lp_sell_price_1 = df_price_summary_lp_1["sell_price"]

            # get price wg from preset 1
            df_price_summary_p2p_1 = df_price_summary.loc[2]
            p2p_buy_price_1 = df_price_summary_p2p_1["buy_price"]
            p2p_sell_price_1 = df_price_summary_p2p_1["sell_price"]

            # get price wg from preset 2
            df_price_summary_wg_2 = df_price_summary.loc[9]
            wg_buy_price_2 = df_price_summary_wg_2["buy_price"]
            wg_sell_price_2 = df_price_summary_wg_2["sell_price"]

            # get price lp from preset 2
            df_price_summary_lp_2 = df_price_summary.loc[10]
            lp_buy_price_2 = df_price_summary_lp_2["buy_price"]
            lp_sell_price_2 = df_price_summary_lp_2["sell_price"]

            # get price lp from preset 2
            df_price_summary_p2p_2 = df_price_summary.loc[11]
            p2p_buy_price_2 = df_price_summary_p2p_2["buy_price"]
            p2p_sell_price_2 = df_price_summary_p2p_2["sell_price"]

            # get price wg from preset 3
            df_price_summary_wg_3 = df_price_summary.loc[12]
            wg_buy_price_3 = df_price_summary_wg_3["buy_price"]
            wg_sell_price_3 = df_price_summary_wg_3["sell_price"]

            # get price lp from preset 3
            df_price_summary_lp_3 = df_price_summary.loc[13]
            lp_buy_price_3 = df_price_summary_lp_3["buy_price"]
            lp_sell_price_3 = df_price_summary_lp_3["sell_price"]

            # get price lp from preset 3
            df_price_summary_p2p_3 = df_price_summary.loc[13]
            p2p_buy_price_3 = df_price_summary_p2p_3["buy_price"]
            p2p_sell_price_3 = df_price_summary_p2p_3["sell_price"]

            buy_price_shop_0 = max(wg_buy_price_1, wg_buy_price_2, wg_buy_price_3)
            sell_price_shop_0 = max(wg_sell_price_1, wg_sell_price_2, wg_sell_price_3)

            buy_price_lp_0 = max(lp_buy_price_1, lp_buy_price_2, lp_buy_price_3)
            sell_price_lp_0 = max(lp_sell_price_1, lp_sell_price_2, lp_sell_price_3)

            buy_price_p2p = min(
                p2p_buy_price_1, p2p_buy_price_2, p2p_buy_price_3, p2p_buy_price
            )
            sell_price_p2p = min(
                p2p_sell_price_1, p2p_sell_price_2, p2p_sell_price_3, p2p_sell_price
            )

            df_wg_price = DataFrame(
                {
                    "id": [8],
                    "symbol_id": [1],
                    "buy_price": [buy_price_shop_0],
                    "sell_price": [sell_price_shop_0],
                }
            )

            df_lp_price = DataFrame(
                {
                    "id": [9],
                    "symbol_id": [1],
                    "buy_price": [buy_price_lp_0],
                    "sell_price": [sell_price_lp_0],
                }
            )

            df_p2p_price = DataFrame(
                {
                    "id": [10],
                    "symbol_id": [1],
                    "buy_price": [buy_price_p2p],
                    "sell_price": [sell_price_p2p],
                }
            )

            df_summary = concat([df_wg_price, df_lp_price, df_p2p_price])
            # print(df_summary)
            update_summary_price(df_summary)

    except Exception as e:
        print(f"Error get_price_summary : {e}")


cal_summary_preset0()
