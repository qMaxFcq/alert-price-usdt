import asyncio
from pandas import concat
from os import getcwd
from sys import path

path.append(getcwd())

from database.get_data import get_usdt_data, get_crypto_data, get_data_ex
from exchange.price_binance import cal_price_binance
from exchange.price_invx import cal_price_invx
from exchange.price_bitkub import cal_price_bitkub
from exchange.price_okx import cal_price_okx
from exchange.price_z import cal_price_z
from exchange.price_btz import cal_price_btz
from exchange.price_xs import cal_price_xs
from exchange.price_binance_th import cal_price_binance_th
from database.update_data import update_price, update_timestamp
from helper.delete_data import check_and_delete
from helper.cal_summary_price_preset0 import cal_summary_preset0
from helper.cal_summary_price_preset1 import cal_summary_preset1
from helper.cal_summary_price_preset2 import cal_summary_preset2
from helper.cal_summary_price_preset3 import cal_summary_preset3
from helper.cal_summary_price_waz import cal_summary_price_waz
from helper.cal_summary_price_19tech import cal_summary_price_19tech


async def fetch_data(fetch_function, *args):
    return await asyncio.to_thread(fetch_function, *args)


async def calculate_price(calc_function, *args):
    return await asyncio.to_thread(calc_function, *args)


async def main():
    update_timestamp()
    raw_usdt_price, raw_crypto_price, exchange_data = await asyncio.gather(
        fetch_data(get_usdt_data), fetch_data(get_crypto_data), fetch_data(get_data_ex)
    )

    (
        binance_price,
        invx_price,
        bk_price,
        btz_price,
        okx_price,
        z_price,
        xs_price,
        binance_th_price,
    ) = await asyncio.gather(
        calculate_price(
            cal_price_binance, raw_usdt_price, raw_crypto_price, exchange_data
        ),
        calculate_price(
            cal_price_invx, raw_usdt_price, raw_crypto_price, exchange_data
        ),
        calculate_price(
            cal_price_bitkub, raw_usdt_price, raw_crypto_price, exchange_data
        ),
        calculate_price(cal_price_btz, raw_usdt_price, exchange_data),
        calculate_price(cal_price_okx, raw_usdt_price, exchange_data),
        calculate_price(cal_price_z, raw_usdt_price, exchange_data),
        calculate_price(cal_price_xs, raw_usdt_price, exchange_data),
        calculate_price(
            cal_price_binance_th, raw_usdt_price, raw_crypto_price, exchange_data
        ),
    )

    combined_df = concat(
        [
            binance_price,
            invx_price,
            bk_price,
            btz_price,
            okx_price,
            z_price,
            xs_price,
            binance_th_price,
        ],
        ignore_index=True,
    )
    update_price(combined_df)
    check_and_delete()
    cal_summary_preset0()
    cal_summary_preset1()
    cal_summary_preset2()
    cal_summary_preset3()
    cal_summary_price_waz()
    cal_summary_price_19tech()

    # print(binance_price)
    # print(invx_price)
    # print(bk_price)
    # print(btz_price)
    # print(okx_price)
    # print(z_price)
    # print(xs_price)
    # print(combined_df)
    # print(binance_th_price)


if __name__ == "__main__":
    asyncio.run(main())
