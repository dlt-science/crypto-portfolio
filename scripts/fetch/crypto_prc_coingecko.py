"""
Script to fetch crypto prices from CoinGecko
"""

import json
import os
import time

from pycoingecko import CoinGeckoAPI
from tqdm import tqdm

from environ.constants import DATA_PATH, PROCESSED_DATA_PATH

cg = CoinGeckoAPI()


# load the dict of crypto list
with open(
    PROCESSED_DATA_PATH / "swiss_quote" / "crypto_lst_exclude_low_vol_and_stable.json",
    "r",
    encoding="utf-8",
) as f:
    processed_crypto_lst = json.load(f)

# check if the folder exists
if not os.path.exists(DATA_PATH / "crypto_prc_coingecko"):
    os.makedirs(DATA_PATH / "crypto_prc_coingecko")

# iterate through the dict
for cyrpto, crypto_info in tqdm(processed_crypto_lst.items()):
    while True:
        time.sleep(5)
        # fetch the market chart
        market_chart = cg.get_coin_market_chart_by_id(
            id=crypto_info["coingecko_id"], vs_currency="usd", days="max"
        )
        if len(crypto_info) > 0:
            break
        time.sleep(5)

    # save the market chart
    with open(
        DATA_PATH / "crypto_prc_coingecko" / f"{cyrpto}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(market_chart, f, ensure_ascii=False, indent=4)
