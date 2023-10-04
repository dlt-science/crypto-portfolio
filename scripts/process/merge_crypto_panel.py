"""
Script to process the crypto data
"""

import json

import pandas as pd

from environ.constants import DATA_PATH, PROCESSED_DATA_PATH

# a dict to store the processed crypto list
df_crypto = {
    "name": [],
    "symbol": [],
    "price": [],
    "timestamp": [],
}

# load the dict of crypto list
with open(
    PROCESSED_DATA_PATH / "swiss_quote" / "crypto_lst_exclude_low_vol_and_stable.json",
    "r",
    encoding="utf-8",
) as f:
    processed_crypto_lst = json.load(f)


# iterate through the dict
for cyrpto_name, crypto_info in processed_crypto_lst.items():
    # load the market chart
    with open(
        DATA_PATH / "crypto_prc_coingecko" / f"{cyrpto_name}.json",
        "r",
        encoding="utf-8",
    ) as f:
        market_chart = json.load(f)

    market_chart_price_list = market_chart["prices"]

    df_crypto["timestamp"] = df_crypto["timestamp"] + [
        _[0] for _ in market_chart_price_list
    ]
    df_crypto["price"] = df_crypto["price"] + [_[1] for _ in market_chart_price_list]
    df_crypto["name"] = df_crypto["name"] + [cyrpto_name] * len(market_chart_price_list)
    df_crypto["symbol"] = df_crypto["symbol"] + [crypto_info["symbol"]] * len(
        market_chart_price_list
    )

# convert the dict to dataframe
df_crypto = pd.DataFrame(df_crypto)
